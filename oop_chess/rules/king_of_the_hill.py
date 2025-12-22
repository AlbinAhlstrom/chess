from oop_chess.enums import GameOverReason
from oop_chess.square import Square
from oop_chess.piece import King
from .standard import StandardRules

class KingOfTheHillRules(StandardRules):
    
    GameOverReason = GameOverReason.load("KingOfTheHill")

    @property
    def name(self) -> str:
        return "King of the Hill"

    def get_game_over_reason(self) -> GameOverReason:
        # Check standard game over reasons first (Checkmate, Stalemate, etc.)
        standard_reason = super().get_game_over_reason()
        if standard_reason != self.GameOverReason.ONGOING:
            return standard_reason

        # Check King of the Hill condition: King on center squares
        center_squares = {Square("d4"), Square("d5"), Square("e4"), Square("e5")}
        
        # Check if current turn player has king on center (unlikely if they just moved, 
        # but theoretically if they moved king there, they win immediately)
        # Actually, the game ends immediately when the move is made. 
        # But this function is usually called after a move.
        # We need to check both kings just to be safe, or just the one who moved.
        # Typically, the player who just moved (previous turn) would have won.
        # But `take_turn` calls `is_game_over`.
        
        for sq, piece in self.state.board.board.items():
            if isinstance(piece, King) and sq in center_squares:
                return self.GameOverReason.KING_ON_HILL
        
        return self.GameOverReason.ONGOING
