import chess
import random 
from bot import get_best_move

board = chess.Board()

while not board.is_game_over():
    print("\nCurrent board:")
    print(board)

    if board.turn == chess.WHITE: # user's turn
        print("\nYour move (e.g., e2e4): ", end="")
        user_input = input()

        try:
            move = chess.Move.from_uci(user_input)
            if move in board.legal_moves:
                board.push(move)
            else:
                print("Illegal move! Try again.")
        except:
            print("Invalid format! Use UCI format like e2e4.")
    else: #bot's turn 
        print("\nBot is thinking...")

        move= get_best_move(board)

        if move not in board.legal_moves:
            print("Bot found an illegal move! This should not happen.")
            continue
        print("Bot's move:", move)
        board.push(move) 

print("\nGame Over!")
print("Result:", board.result())
