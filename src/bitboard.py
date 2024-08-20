ROWS = 8
COLS = 8

def set_bit(bitboard, position):
    return bitboard | (1<<position)

def get_bit(bitboard, position):
    return (bitboard & (1<<position)) >> position

class bitboard:
    def __init__(self):
        self.player_one_pieces = 0
        self.player_two_pieces = 0

        

        self.king_pieces = 0
        

    def print_board(self):
        indicator = 0
        for row in range(ROWS):
            print(indicator, end="")
            for col in range(COLS):
                position = row * 8 + col
                char = self.get_piece_char(position)
                print(f" {char}", end="")
            indicator = indicator + 1
            print()
        print("  ", end="")
        for i in range(COLS):
            print(i, end=" ")
        print()
        print()
    
    def get_piece_char(self, position):
        player_one_bit = get_bit(self.player_one_pieces, position)
        player_two_bit = get_bit(self.player_two_pieces, position)
        king_bit = get_bit(self.king_pieces, position)
        if player_one_bit == 1:
            if king_bit == 1:
                return "A"
            return "a"
        if player_two_bit == 1:
            if king_bit == 1:
                return "B"
            return "b"
        return "." # empty

myboard = bitboard()
myboard.print_board()