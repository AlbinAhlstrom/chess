from board import Color
from pieces import Piece
from pieces.movement import diagonal_moves


class Bishop(Piece):
    """Bishop piece representation.

    Moves any number of squares diagonally.
    """

    def __str__(self):
        match self.color:
            case Color.WHITE:
                return "♗"
            case Color.BLACK:
                return "♝"

    def moves(self):
        return diagonal_moves(self)

    @property
    def value(self):
        return 3
