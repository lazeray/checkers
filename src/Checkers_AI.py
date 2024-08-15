import Board
import random

def get_move(board, player):
    return random_generator(board.get_all_moves(player)) # swap this line out for future algorithms

def random_generator(avaliable_moves):
    return random.choice(avaliable_moves)