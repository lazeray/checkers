from checker import Checker


class Board:
    def __init__(self):
        rows, cols = 8, 8
        self.board = [['0' for _ in range(cols)] for _ in range(rows)]

    def print_board(self):
        for row in self.board:
            print(' '.join(row))
