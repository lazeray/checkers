import bitboard
import random
import sys

MINIMAX_DEPTH = 5

def get_move(board, player):
    return minimax(
        board, player, MINIMAX_DEPTH, -sys.maxsize, sys.maxsize
    )[1]  # swap this out for future algorithms

def random_generator(board, player):
    avaliable_moves = board.get_all_moves(player)
    print(player)
    print(avaliable_moves)
    return random.choice(avaliable_moves)

def minimax_score(board):  # tweak me in the future!
    num__player_one_pieces = board.player_one_pieces.bit_count()
    num_player_one_kings = (board.player_one_pieces & board.king_pieces).bit_count()
    num__player_two_pieces = board.player_two_pieces.bit_count()
    num_player_two_kings = (board.player_two_pieces & board.king_pieces).bit_count()

    return num__player_one_pieces + 0.5 * num_player_one_kings - num__player_two_pieces + 0.5 * num_player_two_kings # temp value funct

def get_opposite_player(player):
    if player == bitboard.Player.PLAYER1:
        return bitboard.Player.PLAYER2
    else:
        return bitboard.Player.PLAYER1



def get_loss_score(player):
    if player == bitboard.Player.PLAYER1:
        return -sys.maxsize
    if player == bitboard.Player.PLAYER2:
        return +sys.maxsize



def minimax(board, player, depth, white_best_val, black_best_val): 
    if board.has_lost(player):
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
        old_p1 = board.player_one_pieces
        old_p2 = board.player_two_pieces
        capture_informations = board.make_moves(moves)
        next_score = minimax(board, next_player, depth - 1, max_score, min_score)[0]
        board.undo_moves(moves, capture_informations)
        if old_p1 != board.player_one_pieces or old_p2 != board.player_two_pieces:
            print("ERRORERRORERROR")
        if player == bitboard.Player.PLAYER1: # pruning section
            if black_best_val < next_score:
                return next_score, None
        if player == bitboard.Player.PLAYER2:
            if white_best_val > next_score:
                return next_score, None

        if next_score > max_score:
            max_score = next_score
            max_moves = moves
        if next_score < min_score:
            min_score = next_score
            min_moves = moves
    if player == bitboard.Player.PLAYER1:
        return max_score, max_moves
    if player == bitboard.Player.PLAYER2:
        return min_score, min_moves

