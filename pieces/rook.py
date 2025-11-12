from board import Color
from pieces import Piece
from pieces.movement import straight_moves


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

    def moves(self):
        return straight_moves(self)

    @property
    def value(self):
        return 5
