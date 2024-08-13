from const import *
from square import Square
from piece import *
from move import Move

class Board:

    def __init__(self):
        # initialize squares
        self.squares = [[0, 0, 0, 0, 0, 0, 0, 0] for col in range(COLS)]
        self._create()
        self._add_pieces('white')
        self._add_pieces('black')

    def knight_moves(self, piece, row, col):
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
                    final = Square(possible_move_row, possible_move_col)

                    move = Move(initial, final)
                    piece.add_move(move)

    def pawn_moves(self, piece, row, col):
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
                    final = Square(move_row, move_col)
                    move = Move(initial, final)
                    piece.add_move(move)

    def calc_moves(self, piece, row, col):
        # calculate all valid moves of a piece

        if piece.name == 'pawn':
            self.pawn_moves(piece, row, col)
        elif piece.name == 'knight':
            self.knight_moves(piece, row, col)

        elif piece.name == 'bishop':
            pass
        elif piece.name == 'rook':
            pass
        elif piece.name == 'queen':
            pass
        elif piece.name == 'king':
            pass 

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
        self.squares[5][3] = Square(5, 3, Pawn(color))

        # knights
        self.squares[row_other][1] = Square(row_other, 1, Knight(color))
        self.squares[row_other][6] = Square(row_other, 6, Knight(color))

        # bishops
        self.squares[row_other][2] = Square(row_other, 2, Bishop(color))
        self.squares[row_other][5] = Square(row_other, 5, Bishop(color))

        # rooks
        self.squares[row_other][0] = Square(row_other, 7, Rook(color))
        self.squares[row_other][7] = Square(row_other, 0, Rook(color))

        # queen
        self.squares[row_other][3] = Square(row_other, 3, Queen(color))

        # king
        self.squares[row_other][4] = Square(row_other, 4, King(color))

# b = Board()
# b._create()