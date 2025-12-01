from chess.piece.piece import SlidingPiece
from chess.enums import Color, Moveset


class Queen(SlidingPiece):
    """Queen piece representation.

    Moves any number of squares, straight or diagonally.
    """

    MOVESET = Moveset.STRAIGHT_AND_DIAGONAL

    def __str__(self):
        match self.color:
            case Color.WHITE:
                return "♕"
            case Color.BLACK:
                return "♛"

    @property
    def value(self):
        return 9

    @property
    def fen(self):
        return "Q" if self.color == Color.WHITE else "q"
