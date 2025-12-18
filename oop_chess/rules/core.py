from abc import ABC, abstractmethod

from oop_chess.enums import Color, MoveLegalityReason, StatusReason, GameOverReason
from oop_chess.game_state import GameState
from oop_chess.move import Move


class Rules(ABC):
    def __init__(self):
        if self.has_check and self.is_check.__func__ == Rules.is_check:
             raise TypeError(f"Class {self.__class__.__name__} has check but does not override is_check.")

    @property
    @abstractmethod
    def name(self) -> str:
        """A unique, human-readable name for this rules variant."""
        ...

    @property
    @abstractmethod
    def fen_type(self) -> str:
        """Specifies the FEN notation used ('standard' or 'x-fen')."""
        ...

    @property
    @abstractmethod
    def has_check(self) -> bool:
        """Indicates if this variant has the concept of 'check'."""
        ...

    @abstractmethod
    def get_legal_moves(self, state: GameState) -> list[Move]:
        """Returns all legal moves in the current state."""
        ...

    @abstractmethod
    def apply_move(self, state: GameState, move: Move) -> GameState:
        """Returns the new state after applying the move."""
        ...

    @abstractmethod
    def validate_move(self, state: GameState, move: Move) -> MoveLegalityReason:
        """Returns the legality reason for a move."""
        ...

    @abstractmethod
    def validate_board_state(self, state: GameState) -> StatusReason:
        """Returns the validity of the board state."""
        ...

    @abstractmethod
    def get_game_over_reason(self, state: GameState) -> GameOverReason:
        """Returns the reason the game is over."""
        ...

    @abstractmethod
    def get_winner(self, state: GameState) -> Color | None:
        """Returns the winner if the game is over, else None."""
        ...

    @abstractmethod
    def get_legal_castling_moves(self, state: GameState) -> list[Move]:
        """Returns legal castling moves for the current state."""
        ...

    @abstractmethod
    def get_legal_en_passant_moves(self, state: GameState) -> list[Move]:
        """Returns legal en passant moves for the current state."""
        ...

    @abstractmethod
    def get_legal_promotion_moves(self, state: GameState) -> list[Move]:
        """Returns legal promotion moves for the current state."""
        ...

    def is_check(self, state: GameState) -> bool:
        """Returns True if the current player is in check.

        If has_check is False, this method returns False.
        If has_check is True, this method MUST be overridden.
        """
        return False
