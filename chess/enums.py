from typing import TYPE_CHECKING
from enum import Enum, StrEnum

if TYPE_CHECKING:
    from chess.square import Square



class Color(StrEnum):
    """Representation of piece/player color.

    Attributes:
        BLACK: Represents black pieces/player.
        WHITE: Represents white pieces/player.
    """

    BLACK = "b"
    WHITE = "w"

    @property
    def opposite(self):
        return Color.BLACK if self == Color.WHITE else Color.WHITE

    def __str__(self):
        return "black" if self.value == "b" else "white"


class CastlingRight(StrEnum):
    """Represents the castling directions a player is allowed."""

    WHITE_SHORT = "K"
    BLACK_SHORT = "k"
    WHITE_LONG = "Q"
    BLACK_LONG = "q"

    @classmethod
    def short(cls, color: Color) -> CastlingRight:
        """Return short castling right by color"""
        if color == Color.WHITE:
            return cls.WHITE_SHORT
        return cls.BLACK_SHORT

    @classmethod
    def long(cls, color: Color) -> CastlingRight:
        """Return long castling right by color"""
        if color == Color.WHITE:
            return cls.WHITE_LONG
        return cls.BLACK_LONG

    @classmethod
    def from_fen(cls, fen_castling_string: str) -> list[CastlingRight]:
        if not fen_castling_string or fen_castling_string == "-":
            return []
        return [cls(char) for char in fen_castling_string]


class Direction(Enum):
    """Directions a piece can move in.

    Enum values are tuples repersenting row and col from an initial board position.
    (x, y) = (col_delta, row_delta)
    """
    NONE = (0, 0)

    UP = (0, -1)
    DOWN = (0, 1)
    LEFT = (-1, 0)
    RIGHT = (1, 0)

    UP_LEFT = (-1, -1)
    UP_RIGHT = (1, -1)
    DOWN_LEFT = (-1, 1)
    DOWN_RIGHT = (1, 1)

    L_UP_LEFT = (-1, -2)
    L_UP_RIGHT = (1, -2)
    L_DOWN_LEFT = (-1, 2)
    L_DOWN_RIGHT = (1, 2)
    L_LEFT_UP = (-2, -1)
    L_LEFT_DOWN = (-2, 1)
    L_RIGHT_UP = (2, -1)
    L_RIGHT_DOWN = (2, 1)

    TWO_LEFT = (-2, 0)
    TWO_RIGHT = (2, 0)

    @classmethod
    def straight(cls) -> set[Direction]:
        return {cls.UP, cls.DOWN, cls.LEFT, cls.RIGHT}

    @classmethod
    def diagonal(cls) -> set[Direction]:
        return {cls.UP_LEFT, cls.DOWN_LEFT, cls.UP_RIGHT, cls.DOWN_RIGHT}

    @classmethod
    def straight_and_diagonal(cls) -> set[Direction]:
        return cls.straight() | cls.diagonal()

    @classmethod
    def two_straight_one_sideways(cls) -> set[Direction]:
        return {
            cls.L_UP_LEFT, cls.L_UP_RIGHT, cls.L_DOWN_LEFT, cls.L_DOWN_RIGHT,
            cls.L_LEFT_UP, cls.L_LEFT_DOWN, cls.L_RIGHT_UP, cls.L_RIGHT_DOWN,
        }

    @classmethod
    def up_straight_or_diagonal(cls) -> set[Direction]:
        return {cls.UP, cls.UP_LEFT, cls.UP_RIGHT}

    @classmethod
    def two_left_or_right(cls) -> set[Direction]:
        return {cls.TWO_LEFT, cls.TWO_RIGHT}

    def get_path(self, square: Square, max_squares: int = 7) -> list[Square]:
        """Get all squares in a direction."""
        return list(self.take_step(square, max_squares))

    def take_step(self, start_square: Square, max_squares: int):
        """
        Generator that yields squares in a specified direction from a start square.
        Stops when the board edge is reached or max_squares is hit.
        """
        from chess.square import Square

        d_col, d_row = self.value

        for dist in range(1, max_squares + 1):
            new_c = start_square.col + (d_col * dist)
            new_r = start_square.row + (d_row * dist)

            if 0 <= new_r < 8 and 0 <= new_c < 8:
                yield Square(new_r, new_c)
            else:
                break

