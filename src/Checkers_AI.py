import Board
import random

def get_move(board, player):
    return random_generator(board, player) # swap this line out for future algorithms

def random_generator(board, player):
    avaliable_moves = board.get_all_moves(player)
    return random.choice(avaliable_moves)