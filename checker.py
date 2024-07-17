class Checker:
    def __init__(self, x, y, char):
        self.is_king = False
        self.x = x
        self.y = y
        self.char = char

    def __str__(self):
        return self.char

    def available_moves(self, board):
        x_change = [0, 1, 0, -1]
        y_change = [1, 0, -1, 0]
        output = []
        for i in range(4):
            new_x = self.x + x_change[i]
            new_y = self.y + y_change[i]
            if 0 > new_x or new_x >= 8 or 0 > new_y >= 8:
                continue
            if board[new_x][new_y] == '0':
                output.append([new_x, new_y])
            new_x += x_change[i]
            new_y += y_change[i]
            if 0 > new_x or new_x >= 8 or 0 > new_y >= 8:
                continue
            if board[new_x][new_y] == '0':
                output.append([new_x, new_y])
        return output

