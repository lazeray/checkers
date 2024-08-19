import Board
import Checkers_AI

human_player = Board.Player.PLAYER1  # can modify this
AI_player = Board.Player.PLAYER2  # can modify this
board = Board.Board()
curr_player = Board.Player.PLAYER1


def AI_move(AI_player):
    moves = Checkers_AI.get_move(board, AI_player)
    print(f"AI moves: {moves}")
    for move in moves:
        board.move(*move)


def human_move(moves):
    for move in moves:
        board.move(*move)

while True:
    board.print_board()
    if board.has_lost(curr_player):
        print(f"{curr_player}  has lost!")
        break

    if curr_player == AI_player:
        AI_move(AI_player)
        curr_player = human_player

    elif curr_player == human_player:
        all_moves = board.get_all_moves(human_player)
        board.print_all_moves(all_moves)
        
        move_index = int(input("Enter the move index: ")) # arguably not brilliant, but it works

        human_move(all_moves[move_index])
        curr_player = AI_player
