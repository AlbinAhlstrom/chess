from typing import Optional
from dataclasses import replace

from oop_chess.board import Board
from oop_chess.game_state import GameState
from oop_chess.move import Move
from oop_chess.rules import Rules, StandardRules
from oop_chess.exceptions import IllegalMoveException, IllegalBoardException
from oop_chess.enums import MoveLegalityReason, Color, StatusReason, GameOverReason


class Game:
    """Represents a chess game.

    Responsible for turn management and history.
    """
    def __init__(self, state: GameState | str | None = None, rules: Rules | None = None):
        if isinstance(state, GameState):
            self.state = state
        elif isinstance(state, str):
            self.state = GameState.from_fen(state)
        elif state is None:
            self.state = GameState.starting_setup()

        self.rules = rules or StandardRules()
        self.history: list[GameState] = []
        self.move_history: list[str] = []

    def add_to_history(self):
        self.history.append(self.state)

    def render(self):
        """Print the board."""
        self.state.board.print()

    def take_turn(self, move: Move):
        """Make a move by finding the corresponding legal move."""
        board_status = self.rules.validate_board_state(self.state)
        if board_status != StatusReason.VALID:
             raise IllegalBoardException(f"Board state is illegal. Reason: {board_status}")

        move_status = self.rules.validate_move(self.state, move)
        if move_status != MoveLegalityReason.LEGAL:
            raise IllegalMoveException(f"Illegal move: {move_status.value}")

        san = move.get_san(self)

        self.add_to_history()
        self.state = self.rules.apply_move(self.state, move)

        # Checkmate/Check annotation relies on rules, but strictly for string formatting.
        # We can keep this or remove it.
        # The user said "remove all Game's references to methods/attributes of Rules"
        # "Let all of that be accessed through game.rules"
        # If I strictly follow this, I shouldn't even call rules inside take_turn?
        # No, take_turn *requires* rules to transition state.
        # But SAN generation checking is_checkmate might be crossing the line?
        # Let's keep the SAN annotation logic minimal.
        
        is_check = self.rules.is_check(self.state)
        is_game_over = self.rules.get_game_over_reason(self.state) != GameOverReason.ONGOING
        
        if is_game_over and is_check:
             san += "#"
        elif is_check:
             san += "+"

        self.move_history.append(san)

    def undo_move(self) -> str:
        """Revert to the previous board state."""
        if not self.history:
            raise ValueError("No moves to undo.")

        self.state = self.history.pop()
        if self.move_history:
            self.move_history.pop()
        print(f"Undo move. Restored FEN: {self.state.fen}")
        return self.state.fen

    @property
    def repetitions_of_position(self) -> int:
        current_fen_key = " ".join(self.state.fen.split()[:4])
        count = 1
        for past_state in self.history:
            past_fen_key = " ".join(past_state.fen.split()[:4])
            if past_fen_key == current_fen_key:
                count += 1
        return count