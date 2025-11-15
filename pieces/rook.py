from chess.pieces import Color, Piece
from chess.pieces.movement import straight_moves


class Rook(Piece):
    """Rook piece representation.

    Moves any number of squares horizontally or vertically.
    """

    def __str__(self):
        match self.color:
            case Color.WHITE:
                return "♖"
            case Color.BLACK:
                return "♜"

    @property
    def moves(self):
        return straight_moves(self)

    @property
    def value(self):
        return 5
