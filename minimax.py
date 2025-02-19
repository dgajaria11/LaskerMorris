import sys
from board import MorrisBoard

def minimax(board, depth, alpha, beta, is_maximizing, player):
    """Minimax algorithm with Alpha-Beta Pruning and state tracking for Lasker Morris."""
    #print(f"DEBUG: Entering minimax: depth={depth}, player={player}", file=sys.stderr)
    #print(f"CALLED MINIMAX WITH depth= {depth}, alpha = {alpha}, ismaxplayer={is_maximizing}, player = {player}")

    if depth == 0 or board.is_terminal():
        eval_score = board.evaluate()
        #print(f"DEBUG: Reached depth 0 or terminal state. Returning eval={eval_score}")
        #print(f"DEBUG: Minimax stopping at depth={depth} with eval={eval_score}", file=sys.stderr)
        return eval_score

    if is_maximizing:
        max_eval = float("-inf")
        for move in board.get_legal_moves():
            board.make_move(move, player)
            eval = minimax(board, depth - 1, alpha, beta, False, "O" if player == "X" else "X")
            board.undo_move(move)  # Properly undo the move

            max_eval = max(max_eval, eval)
            alpha = max(alpha, eval)

            if beta <= alpha:  # Alpha-beta pruning
                #print(f"DEBUG: Pruning at depth={depth} (alpha={alpha}, beta={beta})", file=sys.stderr)
                break

        #print(f"DEBUG: Exiting minimax (maximizing) at depth={depth} with max_eval={max_eval}", file=sys.stderr)
        return max_eval

    else:
        min_eval = float("inf")
        for move in board.get_legal_moves():
            board.make_move(move, player)
            eval = minimax(board, depth - 1, alpha, beta, True, "O" if player == "X" else "X")
            board.undo_move(move)  # Properly undo the move

            min_eval = min(min_eval, eval)
            beta = min(beta, eval)

            if beta <= alpha:  # Alpha-beta pruning
                #print(f"DEBUG: Pruning at depth={depth} (alpha={alpha}, beta={beta})", file=sys.stderr)
                break

        #print(f"DEBUG: Exiting minimax (minimizing) at depth={depth} with min_eval={min_eval}", file=sys.stderr)
        return min_eval

def best_move(board, player, depth=3):
    """Finds the best move using Minimax with Alpha-Beta Pruning."""
    best_score = float("-inf")
    best_move = None

    print(f"DEBUG: Finding best move for {player} at depth={depth}", file=sys.stderr)

    for move in board.get_legal_moves():
        ##board.display()
        board.make_move(move, player)
        #print("board after")
        #board.display()
        score = minimax(board, depth, float("-inf"), float("inf"), False, "O" if player == "X" else "X")
        board.undo_move(move)  # Properly undo the move

        #print(f"DEBUG: Score: {score} with best_score {best_score}")
        if score > best_score:
            best_score = score
            best_move = move
        #print(f"After if score beter: {best_score}")

    print(f"DEBUG: Best move selected: {best_move} with score {best_score}", file=sys.stderr)
    return best_move
