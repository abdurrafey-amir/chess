def print_board(board):
    for row in board:
        print(' '.join(row))

def print_board_with_coordinates(board):
    print('   a b c d e f g h')
    print('  -----------------')
    for i, row in enumerate(board):
        print(f'{8 - i} | {" ".join(row)} | {8 - i}')
    print('  -----------------')
    print('   a b c d e f g h')

def is_valid_move(move):
    if len(move) != 2:
        return False
    if move[0] not in 'abcdefgh' or move[1] not in '12345678':
        return False
    return True

def get_move():
    while True:
        move = input("Enter your move: ")
        if is_valid_move(move):
            return move
        else:
            print("Invalid move. Please try again.")

def make_move(board, move):
    source_square, destination_square = move.split()
    source_row, source_col = int(source_square[1]) - 1, ord(source_square[0]) - ord('a')
    dest_row, dest_col = int(destination_square[1]) - 1, ord(destination_square[0]) - ord('a')
    piece = board[source_row][source_col]
    board[source_row][source_col] = ' '
    board[dest_row][dest_col] = piece



def initialize_board():
    board = [['R', 'N', 'B', 'Q', 'K', 'B', 'N', 'R'],
             ['P', 'P', 'P', 'P', 'P', 'P', 'P', 'P'],
             [' ', ' ', ' ', ' ', ' ', ' ', ' ', ' '],
             [' ', ' ', ' ', ' ', ' ', ' ', ' ', ' '],
             [' ', ' ', ' ', ' ', ' ', ' ', ' ', ' '],
             [' ', ' ', ' ', ' ', ' ', ' ', ' ', ' '],
             ['p', 'p', 'p', 'p', 'p', 'p', 'p', 'p'],
             ['r', 'n', 'b', 'q', 'k', 'b', 'n', 'r']]
    return board

def main():
    board = initialize_board()
    print_board(board)

    def get_move():
        move = input("Enter your move: ")
        return move

    def make_move(board, move):
       
        source_square, destination_square = move.split()
        source_row, source_col = int(source_square[1]) - 1, ord(source_square[0]) - ord('a')
        dest_row, dest_col = int(destination_square[1]) - 1, ord(destination_square[0]) - ord('a')
        piece = board[source_row][source_col]
        board[source_row][source_col] = ' '
        board[dest_row][dest_col] = piece
        




def play_game():
        board = initialize_board()
        while True:
            print_board_with_coordinates(board)
            move = get_move()
            make_move(board, move)

if __name__ == '__main__':
    play_game()