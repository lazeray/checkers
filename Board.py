from enum import Enum

ROWS = 8
COLS = 8


class Player(Enum):
    player1 = 0
    player2 = 1


class Piece(Enum):
    basic = 0
    king = 0


def in_bounds(x, y):
    return 0 <= x < COLS and 0 <= y < ROWS


def is_jump(start_x, end_x):
    return abs(end_x - start_x) > 1


class Board:

    def __init__(self):
        self.player_one_pieces = []
        self.player_two_pieces = []
        for i in range(3):
            for z in range(4):
                checker_x = i
                checker_y = z * 2 + (i + 1) % 2
                temp_piece = self.generate_checker(checker_x, checker_y, Player.player1)
                self.player_one_pieces.append(temp_piece)

                checker_x = i + 5
                checker_y = z * 2 + i % 2
                temp_piece = self.generate_checker(checker_x, checker_y, Player.player2)
                self.player_two_pieces.append(temp_piece)

    def move(self, move):  # move tuple ==> (start_x, start_y, end_x, end_y, Player)
        start_x = move[0]
        start_y = move[1]
        end_x = move[2]
        end_y = move[3]
        player = move[4]

        if is_jump(start_x, end_x):
            self.remove_checker(int((start_x + end_x) / 2), int((start_y + end_y) / 2))  # remove piece

        self.remove_checker(start_x, start_y)
        new_checker = self.generate_checker(end_x, end_y, player)
        self.add_new_checker(new_checker)

    def generate_checker(self, x, y, player): # checker structure ==> (x, y, Player, Piece)
        if y == 0 or y == ROWS:
            return x, y, player, Piece.king
        else:
            return x, y, player, Piece.basic

    def add_new_checker(self, checker):
        if checker[3] == Player.player1:
            self.player_one_pieces.append(checker)
        elif checker[3] == Player.player2:
            self.player_two_pieces.append(checker)

    def print_board(self):
        indicator = 0
        board = self.generate_board()
        for my_row in board:
            print(indicator, end="")
            print(' ', end="")
            print(' '.join(my_row))
            indicator = indicator + 1
        print('  ', end="")
        for i in range(8):
            print(i, end=' ')
        print()

    def get_checker(self, x, y):
        for checker in self.player_one_pieces:
            if checker[0] == x and checker[1] == y:
                return checker
        for checker in self.player_two_pieces:
            if checker[0] == x and checker[1] == y:
                return checker
        return -1  # checker not found at given position

    def remove_checker(self, x, y):
        checker = self.get_checker(x, y)
        if checker[2] == Player.player1:
            self.player_one_pieces.remove(checker)
        elif checker[2] == Player.player2:
            self.player_two_pieces.remove(checker)
        print("something terribly wrong has happened!")  # consider gracefully handling error here
        return 0

    def get_available_moves(self, checker):

        start_x = checker[0]
        start_y = checker[1]
        player = checker[2]
        piece = checker[3]

        x_change = [1, -1, 1, -1]
        y_change = [1, -1, -1, 1]

        if piece is Piece.basic:
            if player is Player.player1:
                x_change = [1, 1]
                y_change = [-1, 1]
            if checker[2] is Player.player2:
                x_change = [-1, -1]
                y_change = [-1, 1]

        moves = []
        for i in range(len(x_change)):
            new_x = start_x + x_change[i]
            new_y = start_y + y_change[i]
            if not in_bounds(new_x, new_y):
                continue
            checker = self.get_checker(new_x, new_y)
            if checker == -1:  # no checker exists at given position
                moves.append((start_x, start_y, new_x, new_y, player))  # move => start_x, start_y, end_x, end_y, Player
            elif checker[2] != player:
                new_x += x_change[i]
                new_y += y_change[i]
                if not in_bounds(new_x, new_y):
                    continue
                if checker == -1:  # no checker exists at given position
                    moves.append((start_x, start_y, new_x, new_y, player))
        return moves

    def print_all_moves(self, player):
        if player == Player.player1:
            for checker in self.player_one_pieces:
                print(self.get_available_moves(checker[0], checker[1]))
        elif player == Player.player2:
            for checker in self.player_two_pieces:
                print(self.get_available_moves(checker[0], checker[1]))

    def generate_board(self):  # perhaps there is a better way of implementing this
        board = [['.' for _ in range(COLS)] for _ in range(ROWS)]
        for checker in self.player_one_pieces:
            if checker[3] == Piece.basic:
                board[checker[0]][checker[1]] = 'a'
            elif checker[3] == Piece.king:
                board[checker[0]][checker[1]] = 'A'
        for checker in self.player_two_pieces:
            if checker[3] == Piece.basic:
                board[checker[0]][checker[1]] = 'b'
            elif checker[3] == Piece.king:
                board[checker[0]][checker[1]] = 'B'
        return board


b = Board()
while True:
    b.print_board()
    row = int(input("enter row: \n"))
    col = int(input("enter col: \n"))
    print(b.get_checker(row, col))  # testing
