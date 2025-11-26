from abc import ABC, abstractmethod
from itertools import chain

from chess.coordinate import Coordinate
from chess.enums import Color, Direction, Moveset


class Piece(ABC):
    """Abstract base class for chess pieces.

    Subclasses must implement 'moves' and 'value' properties, and '__str__'.

    Attributes:
        color: Piece color
        square: Current position on the board, None if captured
        has_moved: True if piece has moved from starting position.
    """

    MOVESET: Moveset = Moveset.NONE
    MAX_SQUARES: int = 7

    def __init__(
        self, color: Color, square: Coordinate | None = None, has_moved: bool = False
    ):
        self.color = color
        self.square = square
        self.has_moved = has_moved

    def __init_subclass__(cls, **kwargs):
        """Require that subclasses define class variable MOVESET."""
        super().__init_subclass__(**kwargs)
        if cls.MOVESET == Moveset.NONE:
            raise NotImplementedError(
                f"Class {cls.__name__} must define class variable MOVESET."
            )

    @property
    @abstractmethod
    def value(self) -> int | float:
        """Return the conventional point value of the piece."""
        ...

    @abstractmethod
    def __str__(self) -> str:
        """Return a unicode symbol for text based visualization."""
        ...

    @property
    @abstractmethod
    def fen(self) -> str:
        """Return the FEN character matching the piece type."""
        ...

    @property
    def css_class(self):
        return f"{self.color}-{self.__class__.__name__.lower()}"

    def _get_moves_in_direction(
        self, direction: Direction, max_steps: int = 8
    ) -> list["Coordinate"]:
        """Generates all theoretical moves along a single vector."""
        possible_moves = []
        d_col, d_row = direction.value

        if self.square is None:
            raise AttributeError("Can't calculate moves for piece with no square.")

        r_curr, c_curr = self.square.row, self.square.col

        for dist in range(1, max_steps + 1):
            new_c = c_curr + (d_col * dist)
            new_r = r_curr + (d_row * dist)

            if 0 <= new_r < 8 and 0 <= new_c < 8:
                possible_moves.append(self.square.__class__(new_r, new_c))
            else:
                break

        return possible_moves

    @property
    def all_directions_array(self):
        """Array of coordinates reachable when moving in all directions"""
        directions = self.MOVESET.value
        max = self.MAX_SQUARES
        return [self._get_moves_in_direction(dir, max) for dir in directions]

    @property
    def pseudo_legal_moves(self) -> list[Coordinate]:
        """All moves legal on an empty board"""
        return list(chain.from_iterable(self.all_directions_array))
