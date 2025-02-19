import random
import sys
class MorrisBoard:
    def __init__(self):
        self.positions = {
            "A1": None, "A4": None, "A7": None,
            "B2": None, "B4": None, "B6": None,
            "C3": None, "C4": None, "C5": None,
            "D1": None, "D2": None, "D3": None, "D5": None, "D6": None, "D7": None,
            "E3": None, "E4": None, "E5": None,
            "F2": None, "F4": None, "F6": None,
            "G1": None, "G4": None, "G7": None
        }
        self.connections = {  # Edges between valid points
            "A1": ["A4", "D1"], "A4": ["A1", "A7", "B4"], "A7": ["A4", "D7"],
            "B2": ["B4", "D2"], "B4": ["B2", "B6", "A4", "C4"], "B6": ["B4", "D6"],
            "C3": ["C4", "D3"], "C4": ["C3", "C5", "B4"], "C5": ["C4", "D5"],
            "D1": ["A1", "G1", "D2"], "D2": ["D1", "D3", "B2", "F2"], "D3": ["D2", "C3", "E3"],
            "D5": ["D6", "C5", "E5"], "D6": ["D5", "D7", "B6", "F6"], "D7": ["D6", "A7", "G7"],
            "E3": ["D3", "E4"], "E4": ["E3", "E5", "C4", "F4"], "E5": ["E4", "D5"],
            "F2": ["D2", "F4"], "F4": ["F2", "F6", "E4"], "F6": ["F4", "D6"],
            "G1": ["D1", "G4"], "G4": ["G1", "G7", "F4"], "G7": ["G4", "D7"]
        }
        self.previous_mills = set()

    def undo_move(self, position):
        """Reverts a move by setting the position back to None."""
        self.positions[position] = None

    def display(self):
        board_visual = f"""
        {self.positions["A1"] or "."}-----------{self.positions["A4"] or "."}-----------{self.positions["A7"] or "."}
        |           |           |
        |   {self.positions["B2"] or "."}-------{self.positions["B4"] or "."}-------{self.positions["B6"] or "."}   |
        |   |       |       |   |
        |   |   {self.positions["C3"] or "."}---{self.positions["C4"] or "."}---{self.positions["C5"] or "."}   |   |
        |   |   |       |   |   |
        {self.positions["D1"] or "."}---{self.positions["D2"] or "."}---{self.positions["D3"] or "."}       {self.positions["D5"] or "."}---{self.positions["D6"] or "."}---{self.positions["D7"] or "."}
        |   |   |       |   |   |
        |   |   {self.positions["E3"] or "."}---{self.positions["E4"] or "."}---{self.positions["E5"] or "."}   |   |
        |   |       |       |   |
        |   {self.positions["F2"] or "."}-------{self.positions["F4"] or "."}-------{self.positions["F6"] or "."}   |
        |           |           |
        {self.positions["G1"] or "."}-----------{self.positions["G4"] or "."}-----------{self.positions["G7"] or "."}
        """
        print(board_visual)


    def make_move(self, position, player):
        if self.positions[position] is None:
            self.positions[position] = player
            return True
        return False

    def remove_piece(self, position):
        self.positions[position] = None  # Remove piece from board

    def get_legal_moves(self):
        return [pos for pos in self.positions if self.positions[pos] is None]

    def is_terminal(self):
        return not any(self.get_legal_moves())  # No moves left = game over

    def evaluate(self):
        """Evaluates the board state for Minimax."""
        score = 0
        ai_player = "X"
        opponent = "O"

        # Count number of pieces
        ai_pieces = sum(1 for v in self.positions.values() if v == ai_player)
        opponent_pieces = sum(1 for v in self.positions.values() if v == opponent)
        score += (ai_pieces - opponent_pieces) * 1  # Weight: 1

        # Count number of mills
        ai_mills = sum(1 for mill in self.get_mills() if all(self.positions.get(p) == ai_player for p in mill))
        opponent_mills = sum(1 for mill in self.get_mills() if all(self.positions.get(p) == opponent for p in mill))
        score += (ai_mills - opponent_mills) * 10  # Weight: 10

        # Debug print before near mill calculation
        #print(f"1. DEBUG: AI Mills: {ai_mills}, Opponent Mills: {opponent_mills}", file=sys.stderr)

        # Check if AI is getting stuck in near-mill calculation
        try:
            ai_near_mills = sum(
                1 for mill in self.get_mills() 
                if sum(1 for p in mill if self.positions.get(p) == ai_player) == 2 
                and sum(1 for p in mill if self.positions.get(p) is None) == 1
            )
        except Exception as e:
            print(f"ERROR in AI near mills: {e}", file=sys.stderr)
            ai_near_mills = 0

        try:
            opponent_near_mills = sum(
                1 for mill in self.get_mills() 
                if sum(1 for p in mill if self.positions.get(p) == opponent) == 2 
                and sum(1 for p in mill if self.positions.get(p) is None) == 1
            )
        except Exception as e:
            print(f"ERROR in Opponent near mills: {e}", file=sys.stderr)
            opponent_near_mills = 0

        score += (ai_near_mills - opponent_near_mills) * 3  # Weight: 3

        # Debug print after near-mill calculation
        #print(f"2. DEBUG: AI Near Mills: {ai_near_mills}, {score} Opponent Near Mills: {opponent_near_mills}", file=sys.stderr)

        return score


    def check_mill(self, position, player):
        """Checks if the given position completes a mill for the player."""
        mill_patterns = [
            ["A1", "A4", "A7"], ["B2", "B4", "B6"], ["C3", "C4", "C5"], 
            ["D1", "D2", "D3"], ["D5", "D6", "D7"], ["E3", "E4", "E5"], 
            ["F2", "F4", "F6"], ["G1", "G4", "G7"],  # Horizontal mills
            ["A1", "D1", "G1"], ["B2", "D2", "F2"], ["C3", "D3", "E3"], 
            ["A4", "B4", "C4"], ["E4", "F4", "G4"], ["C5", "D5", "E5"], 
            ["B6", "D6", "F6"], ["A7", "D7", "G7"]  # Vertical mills
        ]

        for mill in mill_patterns:
            if position in mill and all(self.positions[p] == player for p in mill):
                mill_tuple = tuple(sorted(mill))  # Convert list to tuple for consistency

                # If mill was already formed before, do not count it as new
                if mill_tuple not in self.previous_mills:
                    print(f"DEBUG: New mill formed at {mill_tuple}", file=sys.stderr)
                    self.previous_mills.add(mill_tuple)  # Mark this mill as formed
                    return True  # This is a newly formed mill

        return False  # No new mill was created

    def get_mills(self):
        """Returns all possible mills on the board."""
        return [
            ["A1", "A4", "A7"], ["B2", "B4", "B6"], ["C3", "C4", "C5"], 
            ["D1", "D2", "D3"], ["D5", "D6", "D7"], ["E3", "E4", "E5"], 
            ["F2", "F4", "F6"], ["G1", "G4", "G7"],  # Horizontal mills
            ["A1", "D1", "G1"], ["B2", "D2", "F2"], ["C3", "D3", "E3"], 
            ["A4", "B4", "C4"], ["E4", "F4", "G4"], ["C5", "D5", "E5"], 
            ["B6", "D6", "F6"], ["A7", "D7", "G7"]  # Vertical mills
        ]

    def remove_opponent_piece(self, player):
        """Allows the player (or AI) to remove an opponent's piece when a mill is formed."""
        opponent = "O" if player == "X" else "X"

        # Find all removable opponent pieces (not in a mill)
        removable_pieces = [pos for pos in self.positions if self.positions[pos] == opponent and not self.check_mill(pos, opponent)]

        # If all opponent pieces are in mills, allow removing any
        if not removable_pieces:
            removable_pieces = [pos for pos in self.positions if self.positions[pos] == opponent]

        if removable_pieces:
            print(f"Mill formed! {player}, remove an opponent piece: {removable_pieces}")

            # AI auto-selects a piece instead of prompting for input
            if player == "X":  # AI is playing
                to_remove = random.choice(removable_pieces)  # AI picks randomly (or use a strategy)
                print(f"AI chooses to remove: {to_remove}")
            else:  # Human player input
                while True:
                    to_remove = input(f"Enter position to remove {removable_pieces}: ").strip()
                    if to_remove in removable_pieces:
                        break
                    else:
                        print("Invalid selection, try again.")

            # Remove the selected piece
            self.positions[to_remove] = None
            print(f"Removed {opponent}'s piece from {to_remove}")
