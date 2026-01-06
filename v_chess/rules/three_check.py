from dataclasses import replace
from v_chess.enums import GameOverReason, MoveLegalityReason, BoardLegalityReason, Color
from v_chess.game_state import ThreeCheckGameState
from v_chess.move import Move
from .standard import StandardRules


class ThreeCheckRules(StandardRules):
    """Rules for Three-Check chess variant."""
    MoveLegalityReason = MoveLegalityReason.load("ThreeCheck")
    BoardLegalityReason = BoardLegalityReason.load("ThreeCheck")
    GameOverReason = GameOverReason.load("ThreeCheck")

    @property
    def name(self) -> str:
        """The human-readable name of the variant."""
        return "Three-Check"

    def apply_move(self, move: Move) -> ThreeCheckGameState:
        """Applies a move and updates the check counter."""
        next_state_base = super().apply_move(move)
        
        # Determine current checks from previous state (if it was ThreeCheckGameState)
        current_checks = (0, 0)
        if isinstance(self.state, ThreeCheckGameState):
            current_checks = self.state.checks
            
        # Check if this move GAVE check.
        is_check = next_state_base.rules.is_check()
        
        white_checks, black_checks = current_checks
        
        # The player who JUST moved is self.state.turn.
        if is_check:
            if self.state.turn == Color.WHITE:
                white_checks += 1
            else:
                black_checks += 1
                
        # Create new ThreeCheckGameState
        next_state = ThreeCheckGameState(
            board=next_state_base.board,
            turn=next_state_base.turn,
            castling_rights=next_state_base.castling_rights,
            ep_square=next_state_base.ep_square,
            halfmove_clock=next_state_base.halfmove_clock,
            fullmove_count=next_state_base.fullmove_count,
            rules=next_state_base.rules,
            repetition_count=next_state_base.repetition_count,
            checks=(white_checks, black_checks)
        )
        
        # Re-link rules to the new state subclass
        next_state.rules.state = next_state
        return next_state

    def get_game_over_reason(self) -> GameOverReason:
        """Determines why the game ended, including the 3-check condition."""
        # Check for 3 checks first
        if isinstance(self.state, ThreeCheckGameState):
            if self.state.checks[0] >= 3 or self.state.checks[1] >= 3:
                return self.GameOverReason.THREE_CHECKS
                
        return super().get_game_over_reason()

    def get_winner(self) -> Color | None:
        """Determines the winner of the game."""
        if self.get_game_over_reason() == self.GameOverReason.THREE_CHECKS:
            # Who has 3 checks?
            if isinstance(self.state, ThreeCheckGameState):
                if self.state.checks[0] >= 3:
                    return Color.WHITE
                if self.state.checks[1] >= 3:
                    return Color.BLACK
        return super().get_winner()
