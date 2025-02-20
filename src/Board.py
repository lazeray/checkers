from enum import Enum

ROWS = 8
COLS = 8


class Player(Enum):
    PLAYER1 = 1
    PLAYER2 = 2


class Piece(Enum):
    BASIC = 1
    KING = 2


def is_in_bounds(row, col):
    return 0 <= row < ROWS and 0 <= col < COLS


def move_is_jump(start_row, end_row):
    return abs(end_row - start_row) > 1


def captured_checker_position(start_row, start_col, end_row, end_col):
    return int((start_row + end_row) / 2), int((start_col + end_col) / 2)


def get_player_from_checker(checker):
    return checker[2]


class Board:

    def __init__(self):
        """
        Initializes all pieces in the checkerboard

        @params player_one_pieces: A set representing all of Player 1's pieces
        @params player_two_pieces: A set representing all of Player 2's pieces

        piece = (row, col, player, piece)
        """

        self.player_one_pieces = set()
        self.player_two_pieces = set()
        for row_counter in range(
            int(ROWS / 2) - 1
        ):  # can be tweaked for modifications of the base game
            for col_counter in range(int(COLS / 2)):
                checker_row = row_counter
                checker_col = col_counter * 2 + (row_counter + 1) % 2
                self.player_one_pieces.add(
                    (checker_row, checker_col, Player.PLAYER1, Piece.BASIC)
                )

                checker_row = row_counter + int(ROWS / 2) + 1
                checker_col = col_counter * 2 + row_counter % 2
                self.player_two_pieces.add(
                    (checker_row, checker_col, Player.PLAYER2, Piece.BASIC)
                )

    def move(self, start_row, start_col, end_row, end_col, player):

        if move_is_jump(start_row, end_row):
            self.remove_checker(
                captured_checker_position(start_row, start_col, end_row, end_col)
            )  # remove piece

        self.remove_checker(start_row, start_col)
        new_checker = self.generate_checker(end_row, end_col, player)
        self.add_new_checker(new_checker)

    def generate_checker(
        self, row, col, player
    ):  # checker structure ==> (x, y, Player, Piece)
        if row == 0 or row == ROWS - 1:
            return row, col, player, Piece.KING
        else:
            return row, col, player, Piece.BASIC

    def add_new_checker(self, checker):
        if get_player_from_checker(checker) == Player.PLAYER1:
            self.player_one_pieces.add(checker)
        elif get_player_from_checker(checker) == Player.PLAYER2:
            self.player_two_pieces.add(checker)

    def print_board(self):
        indicator = 0
        board = self.generate_board()
        for my_row in board:
            print(indicator, end="")
            print(" ", end="")
            print(" ".join(my_row))
            indicator = indicator + 1
        print("  ", end="")
        for i in range(COLS):
            print(i, end=" ")
        print()

    def get_checker(self, row, col):
        for checker in self.player_one_pieces:
            if checker[0] == row and checker[1] == col:
                return checker
        for checker in self.player_two_pieces:
            if checker[0] == row and checker[1] == col:
                return checker
        return -1

    def remove_checker(self, row, col):
        checker = self.get_checker(row, col)
        if get_player_from_checker(checker) == Player.PLAYER1:
            self.player_one_pieces.discard(checker)
        elif get_player_from_checker(checker) == Player.PLAYER2:
            self.player_two_pieces.discard(checker)
        raise LookupError(checker + " does not exist in the board")

    def get_available_moves(self, checker):

        start_row = checker[0]
        start_col = checker[1]
        player = checker[2]
        piece = checker[3]

        row_change = [1, -1, 1, -1]
        col_change = [1, -1, -1, 1]

        if piece is Piece.BASIC:
            if player is Player.PLAYER1:
                row_change = [1, 1]
                col_change = [-1, 1]
            if player is Player.PLAYER2:
                row_change = [-1, -1]
                col_change = [-1, 1]

        moves = []
        for i in range(len(row_change)):
            new_row = start_row + row_change[i]
            new_col = start_col + col_change[i]
            if not is_in_bounds(new_row, new_col):
                continue
            checker = self.get_checker(new_row, new_col)
            if checker == -1:  # no checker exists at given position
                moves.append(
                    (start_row, start_col, new_row, new_col, player)
                )  # move => start_x, start_y, end_x, end_y, Player
            elif get_player_from_checker(checker) != player:  # next checker is jumpable
                new_row += row_change[i]
                new_col += col_change[i]
                if not is_in_bounds(new_row, new_col):
                    continue
                if checker == -1:  # no checker exists at given position
                    moves.append((start_row, start_col, new_row, new_col, player))
        return moves

    def print_all_moves(self, player):
        if player == Player.PLAYER1:
            for checker in self.player_one_pieces:
                print(self.get_available_moves(checker))
        elif player == Player.PLAYER2:
            for checker in self.player_two_pieces:
                print(self.get_available_moves(checker))

    def generate_board(self):  # perhaps there is a better way of implementing this
        board = [["." for _ in range(COLS)] for _ in range(ROWS)]
        for checker in self.player_one_pieces:
            piece = checker[3]
            if piece == Piece.BASIC:
                board[checker[0]][checker[1]] = "a"
            elif piece == Piece.KING:
                board[checker[0]][checker[1]] = "A"
        for checker in self.player_two_pieces:
            if piece == Piece.BASIC:
                board[checker[0]][checker[1]] = "b"
            elif piece == Piece.KING:
                board[checker[0]][checker[1]] = "B"
        return board


b = Board()
while True:
    b.print_board()
    b.print_all_moves(Player.PLAYER1)
    row = int(input("enter row: \n"))
    col = int(input("enter col: \n"))
