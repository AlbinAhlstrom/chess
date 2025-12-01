from chess.piece.piece import SlidingPiece
from chess.enums import Color, Moveset


class Rook(SlidingPiece):
    """Rook piece representation.

    Moves any number of squares horizontally or vertically.
    """

    MOVESET = Moveset.STRAIGHT

    def __str__(self) -> str:
        match self.color:
            case Color.WHITE:
                return "♖"
            case Color.BLACK:
                return "♜"

    @property
    def value(self):
        return 5

    @property
    def fen(self):
        return "R" if self.color == Color.WHITE else "r"
