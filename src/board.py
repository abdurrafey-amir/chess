from const import *
from square import Square
from piece import *
from move import Move
import copy
from sound import Sound
import os

class Board:

    def __init__(self):
        # initialize squares
        self.squares = [[0, 0, 0, 0, 0, 0, 0, 0] for col in range(COLS)]
        self._create()
        self._add_pieces('white')
        self._add_pieces('black')
        self.last_move = None

    def knight_moves(self, piece, row, col, bool):
        possible_moves = [
            (row-2, col+1),
            (row-1, col+2),
            (row+1, col+2),
            (row+2, col+1),
            (row+2, col-1),
            (row+1, col-2),
            (row-1, col-2),
            (row-2, col-1)
        ]

        for possible_move in possible_moves:
            possible_move_row, possible_move_col = possible_move
            
            if Square.in_range(possible_move_row, possible_move_col):
                if self.squares[possible_move_row][possible_move_col].isempty_or_rival(piece.color):
                    initial = Square(row, col)
                    final_piece = self.squares[possible_move_row][possible_move_col].piece
                    final = Square(possible_move_row, possible_move_col, final_piece)

                    move = Move(initial, final)
                    # check
                    if bool:
                        if not self.in_check(piece, move):
                            piece.add_move(move)
                        else:
                            break
                    else:
                        piece.add_move(move)

    def pawn_moves(self, piece, row, col, bool):
        # if piece.moved:
        #     steps = 1
        # else:
        #     steps = 2
        steps = 1 if piece.moved else 2

        start = row + piece.dir
        finish = row + (piece.dir * (1 + steps))
        
        for move_row in range(start, finish, piece.dir):
            if Square.in_range(move_row):
                if self.squares[move_row][col].isempty():
                    initial = Square(row, col)
                    final = Square(move_row, col)
                    move = Move(initial, final)

                    # if not in check
                    if bool:
                        if not self.in_check(piece, move):
                            piece.add_move(move)
                    else:
                        piece.add_move(move)
                else:
                    break
            else:
                break

        # diagonal movement
        move_row = row + piece.dir
        move_cols = [col-1, col+1]
        for move_col in move_cols:
            if Square.in_range(move_row, move_col):
                if self.squares[move_row][move_col].has_rival_piece(piece.color):
                    initial = Square(row, col)
                    final_piece = self.squares[move_row][move_col].piece
                    final = Square(move_row, move_col, final_piece)
                    move = Move(initial, final)
                    # check
                    if bool:
                        if not self.in_check(piece, move):
                            piece.add_move(move)
                    else:
                        piece.add_move(move)

        # en passant moves
        r = 3 if piece.color == 'white' else 4
        finalr = 2 if piece.color == 'white' else 5
        
        # left en passant
        if Square.in_range(col-1) and row == r:
            if self.squares[row][col-1].has_rival_piece(piece.color):
                p = self.squares[row][col-1].piece
                if isinstance(p, Pawn):
                    if p.passant:
                        initial = Square(row, col)
                        final = Square(finalr, col-1, p)
                        move = Move(initial, final)

                        if bool:
                            if not self.in_check(piece, move):
                                piece.add_move(move)
                        else:
                            piece.add_move(move)


        # right en passant
        if Square.in_range(col+1) and row == r:
            if self.squares[row][col+1].has_rival_piece(piece.color):
                p = self.squares[row][col+1].piece
                if isinstance(p, Pawn):
                    if p.passant:
                        initial = Square(row, col)
                        final = Square(finalr, col+1, p)
                        move = Move(initial, final)

                        if bool:
                            if not self.in_check(piece, move):
                                piece.add_move(move)
                        else:
                            piece.add_move(move)




    def other_moves(self, piece, row, col, increments, bool):
        for inc in increments:
            row_inc, col_inc = inc
            move_row = row + row_inc
            move_col = col + col_inc

            while True:
                if Square.in_range(move_row, move_col):
                    
                    initial = Square(row, col)
                    final_piece = self.squares[move_row][move_col].piece
                    final = Square(move_row, move_col, final_piece)

                    move = Move(initial, final)

                    if self.squares[move_row][move_col].isempty():
                        if bool:
                            if not self.in_check(piece, move):
                                piece.add_move(move)
                        else:
                            piece.add_move(move)


                    elif self.squares[move_row][move_col].has_rival_piece(piece.color):
                        if bool:
                            if not self.in_check(piece, move):
                                piece.add_move(move)
                        else:
                            piece.add_move(move)
                        break

                    elif self.squares[move_row][move_col].has_team_piece(piece.color):
                        break

                else: 
                    break

                move_row, move_col = move_row + row_inc, move_col + col_inc

    def king_moves(self, piece, row, col, bool):
        perp = [
            (row-1, col+0),
            (row-1, col-1),
            (row-1, col+1),
            (row+1, col+1),
            (row+0, col+1),
            (row+1, col-1),
            (row+1, col+0),
            (row+0, col-1)
        ]

        for move in perp:
            
            move_row, move_col = move

            if Square.in_range(move_row, move_col):
                if self.squares[move_row][move_col].isempty_or_rival(piece.color):
                    initial = Square(row, col)
                    final = Square(move_row, move_col)

                    move = Move(initial, final)

                    if bool:
                        if not self.in_check(piece, move):
                            piece.add_move(move)
                        else:
                            break
                    else:
                        piece.add_move(move)


        # castling
        if not piece.moved:
            
            # queen castling
             if 0 <= row <= 7 and 0 <= 0 <= 7:
                left_rook = self.squares[row][0].piece

                if isinstance(left_rook, Rook):
                    if not left_rook.moved:
                        for c in range(1, 4):
                            # break if there is a piece in the way
                            if self.squares[row][c].has_piece():
                                break
                            if c == 3:
                                piece.left_rook = left_rook

                                # rook
                                initial = Square(row, 0)
                                final = Square(row, 3)
                                moveR = Move(initial, final)
                                

                                # king
                                initial = Square(row, col)
                                final = Square(row, 2)
                                moveK = Move(initial, final)
                                

                                if bool:
                                    if not self.in_check(piece, moveK) and not self.in_check(left_rook, moveR):
                                        piece.add_move(moveK)
                                        left_rook.add_move(moveR)
                                else:
                                    piece.add_move(moveK)
                                    left_rook.add_move(moveR)


            # king castling
                if 0 <= row <= 7 and 0 <= 7 <= 7:
                    right_rook = self.squares[row][0].piece
                    
                    if isinstance(right_rook, Rook):
                        if not right_rook.moved:
                            for c in range(5, 7):
                                # break if there is a piece in the way
                                if self.squares[row][c].has_piece():
                                    break
                                if c == 6:
                                    piece.right_rook = right_rook

                                    # rook
                                    initial = Square(row, 7)
                                    final = Square(row, 5)
                                    moveR = Move(initial, final)
                                    

                                    # king
                                    initial = Square(row, col)
                                    final = Square(row, 6)
                                    moveK = Move(initial, final)
                                    


                                    if bool:
                                        if not self.in_check(piece, moveK) and not self.in_check(right_rook, moveR):
                                            piece.add_move(moveK)
                                            right_rook.add_move(moveR)
                                    else:
                                        piece.add_move(moveK)
                                        right_rook.add_move(moveR)




    def calc_moves(self, piece, row, col, bool=True):
        # calculate all valid moves of a piece

        if piece.name == 'pawn':
            self.pawn_moves(piece, row, col, bool)

        elif piece.name == 'knight':
            self.knight_moves(piece, row, col, bool)

        elif piece.name == 'bishop':
            self.other_moves(piece, row, col, [
                (-1, 1),
                (1, -1),
                (-1, -1),
                (1, 1)
            ], bool)

        elif piece.name == 'rook':
            self.other_moves(piece, row, col, [
                (-1, 0),
                (0, 1),
                (1, 0),
                (0, -1)
            ], bool)

        elif piece.name == 'queen':
            self.other_moves(piece, row, col, [
                (-1, 1), # merge bishop and rook increments
                (1, -1),
                (-1, -1),
                (1, 1),
                (-1, 0),
                (0, 1),
                (1, 0),
                (0, -1)
            ], bool)

        elif piece.name == 'king':
            self.king_moves(piece, row, col, bool)

    def check_promo(self, piece, final):
        if final.row == 0 or final.row == 7:
            self.squares[final.row][final.col].piece = Queen(piece.color)
    
    def castling(self, initial, final):
        return abs(initial.col - final.col) == 2

    def passant_true(self, piece):
        if not isinstance(piece, Pawn):
            return 
        
        for row in range(ROWS):
            for col in range(COLS):
                if self.squares[row][col].has_rival_piece(piece.color):
                    rival = self.squares[row][col].piece
                    if isinstance(rival, Pawn):
                        rival.passant = False

        piece.passant = True

    def move(self, piece, move, sound=False):
        initial = move.initial
        final = move.final

        passant_empty = self.squares[final.row][final.col].isempty()

        self.squares[initial.row][initial.col].piece = None
        self.squares[final.row][final.col].piece = piece

        # pawn
        if isinstance(piece, Pawn):

            # en passant capture
            diff = final.col - initial.col
            if diff != 0 and passant_empty:
                self.squares[initial.row][initial.col + diff].piece = None
                self.squares[final.row][final.col].piece = piece
                if not sound:
                    sound = Sound(os.path.join('assets/sounds', 'capture.wav'))
                    sound.play()

            
            # pawn promotion
            else:
                self.check_promo(piece, final)


        # king castling
        if isinstance(piece, King):
            if self.castling(initial, final):# and not sound:
                diff = final.col - initial.col
                rook = piece.left_rook if diff < 0 else piece.right_rook
                if rook.moves:
                    self.move(rook, rook.moves[-1])
            

        piece.moved = True
        piece.clear_moves()
        self.last_move = move

    def valid_move(self, piece, move):
        return move in piece.moves

    def in_check(self, piece, move):
        temp_board = copy.deepcopy(self)
        temp_piece = copy.deepcopy(piece)
        temp_board.move(temp_piece, move, sound=True)

        for row in range(ROWS):
            for col in range(COLS):
                if temp_board.squares[row][col].has_rival_piece(piece.color):
                    piece1 = temp_board.squares[row][col].piece
                    temp_board.calc_moves(piece1, row, col, bool=False)
                    for temp_move in piece1.moves:
                        if isinstance(temp_move.final.piece, King):
                            return True
        
        return False

    def _create(self):
        # self.squares = [[0, 0, 0, 0, 0, 0, 0, 0] for col in range(COLS)]
        # print(self.squares)
        
        # add squares to the board
        for row in range(ROWS):
            for col in range(COLS):
                self.squares[row][col] = Square(row, col)

    def _add_pieces(self, color):
        # if color == 'white':
        #     row_pawn, row_other = (6, 7)
        # else:
        #     row_pawn, row_other = (1, 0)
        
        row_pawn, row_other = (6, 7) if color == 'white' else (1, 0)

        # pawns
        for col in range(COLS):
            self.squares[row_pawn][col] = Square(row_pawn, col, Pawn(color))
        # self.squares[5][3] = Square(5, 3, Pawn(color))

        # knights
        self.squares[row_other][1] = Square(row_other, 1, Knight(color))
        self.squares[row_other][6] = Square(row_other, 6, Knight(color))

        # bishops
        self.squares[row_other][2] = Square(row_other, 2, Bishop(color))
        self.squares[row_other][5] = Square(row_other, 5, Bishop(color))
        # self.squares[5][7] = Square(5, 7, Bishop(color))
        # self.squares[3][4] = Square(3, 4, Bishop(color))

        # rooks
        self.squares[row_other][0] = Square(row_other, 7, Rook(color))
        self.squares[row_other][7] = Square(row_other, 0, Rook(color))

        # queen
        self.squares[row_other][3] = Square(row_other, 3, Queen(color))

        # king
        self.squares[row_other][4] = Square(row_other, 4, King(color))
        # self.squares[5][3] = Square(5, 3, King(color))

# b = Board()
# b._create()