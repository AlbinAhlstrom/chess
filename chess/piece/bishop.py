from chess.piece.piece import Piece
from chess.enums import Color, Moveset


class Bishop(Piece):
    """Bishop piece representation.

    Moves any number of squares diagonally.
    """

    MOVESET = Moveset.DIAGONAL

    def __str__(self):
        match self.color:
            case Color.WHITE:
                return "♗"
            case Color.BLACK:
                return "♝"

    @property
    def value(self):
        return 3

    @property
    def fen(self):
        return "B" if self.color == Color.WHITE else "b"
