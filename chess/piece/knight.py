from chess.enums import Color, Moveset
from chess.piece.piece import SteppingPiece
from chess.square import Square


class Knight(SteppingPiece):
    """Knight piece representation.

    Moves two squares in one direction and one square perpendicular.
    """

    MOVESET = Moveset.KNIGHT

    def __str__(self):
        match self.color:
            case Color.WHITE:
                return "♘"
            case Color.BLACK:
                return "♞"

    @property
    def value(self):
        return 3

    @property
    def fen(self):
        return "N" if self.color == Color.WHITE else "n"
