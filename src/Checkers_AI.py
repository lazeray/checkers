import Board
import random
import copy
import sys

MINIMAX_DEPTH = 3


def get_move(board, player):
    return minimax(
        board, player, MINIMAX_DEPTH
    )[1]  # swap this line out for future algorithms


def minimax_score(board):  # tweak me in the future!
    player1_pieces = len(board.player_one_pieces)
    player2_pieces = len(board.player_two_pieces)
    return (
        player1_pieces - player2_pieces
    )  # player 1 wants to maximize the score, player2 wants to minimize the score


def get_opposite_player(player):
    if player == Board.Player.PLAYER1:
        return Board.Player.PLAYER2
    else:
        return Board.Player.PLAYER1


def has_lost(board, player):
    if player == Board.Player.PLAYER1 and len(board.player_one_pieces) == 0:
        return True
    if player == Board.Player.PLAYER2 and len(board.player_two_pieces) == 0:
        return True
    if board.get_all_moves(player) == []:
        return True
    return False

def get_loss_score(player):
    if player == Board.Player.PLAYER1:
        return sys.maxsize
    if player == Board.Player.PLAYER2:
        return -sys.maxsize

def get_resulting_boardstate( # perhaps i should implement this inside the Board.py class
    board, moves
):  # this is bad for runtime. Maybe i should implement an undo function but that sounds really awful
    board_copy = copy.deepcopy(board)
    print(moves)
    for move in moves:
        board_copy.move(*move)
    return board_copy


def minimax(board, player, depth):  # TODO implement alpha-beta pruning
    if has_lost(board, player):
        return get_loss_score(player), None
    if depth == 0:
        return minimax_score(board), None
    avaliable_moves = board.get_all_moves(player)
    max_score = -sys.maxsize
    min_score = sys.maxsize
    max_moves = -1
    min_moves = -1

    for moves in avaliable_moves:
        next_player = get_opposite_player(player)
        next_board = get_resulting_boardstate(board, moves)
        next_score = minimax(next_board, next_player, depth - 1)[0]
        if next_score > max_score:
            max_score = next_score
            max_moves = moves
        if next_score < min_score:
            min_score = next_score
            min_moves = moves
    if player == Board.Player.PLAYER1:
        return max_score, max_moves
    if player == Board.Player.PLAYER2:
        return min_score, min_moves


def random_generator(board, player):
    avaliable_moves = board.get_all_moves(player)
    return random.choice(avaliable_moves)
