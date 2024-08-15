import Board
import Checkers_AI

human_player = Board.Player.PLAYER2 # can modify this
AI_player = Board.Player.PLAYER1 # can modify this 
board = Board.Board()
curr_player = Board.Player.PLAYER1

def AI_move(AI_player):
    moves = Checkers_AI.get_move(board, AI_player)
    for move in moves:
        board.move(*move)

def human_move(start_row, start_col, end_row, end_col, human_player):
    board.move(start_row, start_col, end_row, end_col, human_player)




while True:
    board.print_board()
    if curr_player is AI_player:
        AI_move(AI_player)
        curr_player = human_player
    elif curr_player is human_player:
        print(board.get_all_moves(human_player))
        # take inputs
        start_row = int(input("Enter the start_row: "))
        start_col = int(input("Enter the start_col: "))
        end_row = int(input("Enter the end_row: "))
        end_col = int(input("Enter the end_col: "))
        human_move(start_row, start_col, end_row, end_col, human_player)
        print(board.get_all_moves(human_player))
        curr_player = AI_player