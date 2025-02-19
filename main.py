from board import MorrisBoard
from game_logic import switch_player, check_winner
from minimax import best_move
from config import BLUE, ORANGE

def test_game():
    board = MorrisBoard()
    current_player = BLUE

    while True:
        board.display()
        print(f"Player {current_player}, it's your turn.")

        # Get player's move (either from AI or user)
        
        if current_player == BLUE:
            move = best_move(board, BLUE)
            #move = "A1"
            print(f"AI chooses: {move}")
        else:
            move = input(f"Enter your move {board.get_legal_moves()}: ").strip()

        if move in board.get_legal_moves():
            board.make_move(move, current_player)

            # Check if a mill was formed
            if board.check_mill(move, current_player):
                board.remove_opponent_piece(current_player)  # Remove an opponent's piece

        else:
            print("Invalid move, try again.")
            continue

        # Check for winner
        winner = check_winner(board)
        if winner:
            board.display()
            print(f"Game Over! Winner: {winner}")
            break

        current_player = switch_player(current_player)  # Switch turns
import sys
from board import MorrisBoard
from minimax import best_move

# Map referee's colors to AI's symbols
REFEREE_TO_AI = {"blue": "X", "orange": "O"}
AI_TO_REFEREE = {v: k for k, v in REFEREE_TO_AI.items()}

def main():
    board = MorrisBoard()

    # Read initial color from referee ("blue" or "orange")
    player_color = input().strip()
    ai_symbol = REFEREE_TO_AI[player_color]  # Convert to AI symbol ("X" or "O")
    opponent_symbol = "O" if ai_symbol == "X" else "X"

    while True:
        try:
            # Read opponent's move or game start signal
            game_input = input().strip()

            if game_input != "start":
                # Convert opponent's move from referee format to board format
                board.make_move(game_input, opponent_symbol)

            # Display board for debugging (optional)
            # board.display()

            # AI determines the best move
            move = best_move(board, ai_symbol)


            # Convert AI's move back to referee format and send it
            print(move, flush=True)

            # Make the move on the board
            board.make_move(move, ai_symbol)
        except EOFError:
            break

if __name__ == "__main__":
    test_game()
