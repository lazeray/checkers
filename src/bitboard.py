from enum import Enum

ROWS = 8
COLS = 8

class Player(Enum):
    PLAYER1 = 1
    PLAYER2 = 2

def set_bit(bitboard, row, col):
    position = row * ROWS + col
    return bitboard | (1<<position)

def del_bit(bitboard, row, col):
    position = row * ROWS + col
    return bitboard & ~(1<<position)

def get_bit(bitboard, row, col):
    position = row * ROWS + col
    return (bitboard & (1<<position)) >> position

def get_opposite_player(player):
    if player == Player.PLAYER1:
        return Player.PLAYER2
    else:
        return Player.PLAYER1

def move_is_jump(start_row, end_row):
    return abs(end_row - start_row) > 1

def get_captured_checker_position(start_row, start_col, end_row, end_col):
    return int((start_row + end_row) / 2), int((start_col + end_col) / 2)

def is_in_bounds(row, col):
    return 0 <= row < ROWS and 0 <= col < COLS


class bitboard:
    def __init__(self):
        self.player_one_pieces = 0
        self.player_two_pieces = 0
        self.king_pieces = 0

        for row_counter in range(
            int(ROWS / 2) - 1
        ):  # there is a more bit-operation esque way of doing this as well
            for col_counter in range(int(COLS / 2)):
                checker_row = row_counter
                checker_col = col_counter * 2 + (row_counter + 1) % 2
                self.player_one_pieces = set_bit(self.player_one_pieces, checker_row, checker_col)

                checker_row = row_counter + int(ROWS / 2) + 1
                checker_col = col_counter * 2 + row_counter % 2
                self.player_two_pieces = set_bit(self.player_two_pieces, checker_row, checker_col)
        

    def print_board(self):
        indicator = 0
        for row in range(ROWS):
            print(indicator, end="")
            for col in range(COLS):
                char = self.get_piece_char(row, col)
                print(f" {char}", end="")
            indicator = indicator + 1
            print()
        print("  ", end="")
        for i in range(COLS):
            print(i, end=" ")
        print()
        print()
    
    def get_piece_char(self, row, col): # print_board helper function
        player_one_bit = get_bit(self.player_one_pieces, row, col)
        player_two_bit = get_bit(self.player_two_pieces, row, col)
        king_bit = get_bit(self.king_pieces, row, col)
        if player_one_bit == 1:
            if king_bit == 1:
                return "A"
            return "a"
        if player_two_bit == 1:
            if king_bit == 1:
                return "B"
            return "b"
        return "." # empty

    def get_bitboard(self, player):
        if player == Player.PLAYER1:
            return self.player_one_pieces
        if player == Player.PLAYER2:
            return self.player_two_pieces

    def move(self, start_row, start_col, end_row, end_col, player):
        original_is_king = False
        captured_is_king = False
        working_bitboard = self.get_bitboard(player)
        opposite_bitboard = self.get_bitboard(get_opposite_player(player))
        if move_is_jump(start_row, end_row):
            opposite_bitboard = del_bit(opposite_bitboard, *get_captured_checker_position(start_row, start_col, end_row, end_col))
            if get_bit(self.king_pieces, *get_captured_checker_position(start_row, start_col, end_row, end_col)) == 1:
                captured_is_king = True
            self.king_pieces = del_bit(self.king_pieces, *get_captured_checker_position(start_row, start_col, end_row, end_col))
    
        if get_bit(self.king_pieces, start_row, start_col) == 1 or end_row == 0 or end_row == ROWS - 1: # if piece was a king, or will promote
            self.king_pieces = set_bit(self.king_pieces, end_row, end_col) # the place where it moves should be a king
        working_bitboard = set_bit(working_bitboard, end_row, end_col)

        if get_bit(self.king_pieces, start_row, start_col) == 1:
            original_is_king = True
        self.king_pieces = del_bit(self.king_pieces, start_row, start_col)
        working_bitboard = del_bit(working_bitboard, start_row, start_col)

        if player == Player.PLAYER1:
            self.player_one_pieces = working_bitboard
            self.player_two_pieces = opposite_bitboard
        if player == Player.PLAYER2:
            self.player_two_pieces = working_bitboard
            self.player_one_pieces = opposite_bitboard

        return captured_is_king, original_is_king # necessary information to use the undo function

    def undo(self, start_row, start_col, end_row, end_col, player, captured_was_king, original_was_king):
        working_bitboard = self.get_bitboard(player)
        opposite_bitboard = self.get_bitboard(get_opposite_player(player))

        if move_is_jump(start_row, end_row):
            opposite_bitboard = set_bit(opposite_bitboard, *get_captured_checker_position(start_row, start_col, end_row, end_col))
            if captured_was_king:
                self.king_pieces = set_bit(self.king_pieces, *get_captured_checker_position(start_row, start_col, end_row, end_col))

        working_bitboard = set_bit(working_bitboard, start_row, start_col)
        if original_was_king:
            self.king_pieces = set_bit(self.king_pieces, start_row, start_col)

        self.king_pieces = del_bit(self.king_pieces, end_row, end_col)
        working_bitboard = del_bit(working_bitboard, end_row, end_col)

        if player == Player.PLAYER1:
            self.player_one_pieces = working_bitboard
            self.player_two_pieces = opposite_bitboard
        if player == Player.PLAYER2:
            self.player_two_pieces = working_bitboard
            self.player_one_pieces = opposite_bitboard

    def make_moves(self, moves):
        capture_informations = []
        for move in moves:
            capture_informations.append(self.move(*move))
        return capture_informations
    
    def undo_moves(self, moves, capture_informations):
        for move, capture_info in zip(reversed(moves), reversed(capture_informations)):
            self.undo(*move, *capture_info)

    def get_available_moves(self, row, col):
        return self.get_regular_moves(row, col) + self.get_jump_moves(row,col)
        
    def get_jump_moves(self, row, col):
        is_king = (get_bit(self.king_pieces, row, col) == 1)
        player = self.get_player(row, col)
        row_change = [2, -2, 2, -2]
        col_change = [2, -2, -2, 2]
        if not is_king:
            if player == Player.PLAYER1:
                row_change = [2, 2]
                col_change = [-2, 2]
            if player == Player.PLAYER2:
                row_change = [-2, -2]
                col_change = [-2, 2]
    
        moves = []
        for i in range(len(row_change)):
            new_row = row + row_change[i]
            new_col = col + col_change[i]
            if not is_in_bounds(new_row, new_col):
                continue
            captured_checker_position = get_captured_checker_position(row, col, new_row, new_col)
            if self.get_player(new_row, new_col) == -1 and self.get_player(*captured_checker_position) == get_opposite_player(player):
                capture_information = self.move(row, col, new_row, new_col, player)
                future_moves = self.get_jump_moves(new_row, new_col)
                if future_moves == []:
                    move_wrapper = []
                    move_wrapper.append((row, col, new_row, new_col, player))
                    moves.append(move_wrapper)
                else:
                    for move in future_moves:
                        move_wrapper = []
                        move_wrapper.append((row, col, new_row, new_col, player))
                        move_wrapper.extend(move)
                        moves.append(move_wrapper)

                self.undo(row, col, new_row, new_col, player, *capture_information)

        return moves

    def get_regular_moves(self, row, col):

        is_king = (get_bit(self.king_pieces, row, col) == 1)
        player = self.get_player(row, col)

        row_change = [1, -1, 1, -1]
        col_change = [1, -1, -1, 1]
        if not is_king:
            if player == Player.PLAYER1:
                row_change = [1, 1]
                col_change = [-1, 1]
            if player == Player.PLAYER2:
                row_change = [-1, -1]
                col_change = [-1, 1]
        
        moves = []
        for i in range(len(row_change)):
            new_row = row + row_change[i]
            new_col = col + col_change[i]
            if not is_in_bounds(new_row, new_col):
                continue
            if self.get_player(new_row, new_col) == -1: # no checker exists at given position
                move_wrapper = []
                move_wrapper.append((row, col, new_row, new_col, player))
                moves.append(
                    move_wrapper
                )  # move => start_x, start_y, end_x, end_y, Player
        return moves

    def get_player(self, row, col):
        if get_bit(self.player_one_pieces, row, col) == 1:
            return Player.PLAYER1
        if get_bit(self.player_two_pieces, row, col) == 1:
            return Player.PLAYER2
        return -1 # no piece exists at given position

    def get_all_moves(self, player):
        all_moves = []
        working_bitboard = self.get_bitboard(player)
        
        for row in range(ROWS):
            for col in range(COLS):
                if get_bit(working_bitboard, row, col) == 1: # ditto
                        for move in self.get_available_moves(row, col):
                            all_moves.append(move)
                    

        return all_moves
    
    def print_all_moves(self, all_moves):
        for index, move in enumerate(all_moves):
            print(f"{index}: {move}")


    def has_lost(self, player):
        if player == Player.PLAYER1 and self.player_one_pieces == 0:
            return True
        if player == Player.PLAYER2 and self.player_two_pieces == 0:
            return True
        if self.get_all_moves(player) == []:
            return True
        return False
