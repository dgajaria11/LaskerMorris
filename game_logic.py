from board import MorrisBoard
from minimax import best_move
from config import BLUE, ORANGE

def switch_player(player):
    return ORANGE if player == BLUE else BLUE

def check_winner(board):
    if board.is_terminal():
        blue_score = sum(1 for v in board.positions.values() if v == BLUE)
        orange_score = sum(1 for v in board.positions.values() if v == ORANGE)
        if blue_score > orange_score:
            return BLUE
        elif orange_score > blue_score:
            return ORANGE
    return None
