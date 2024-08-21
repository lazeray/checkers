import bitboard
import random

def random_generator(board, player):
    avaliable_moves = board.get_all_moves(player)
    print(player)
    print(avaliable_moves)
    return random.choice(avaliable_moves)


def get_move(board, player):
    return random_generator(board, player)