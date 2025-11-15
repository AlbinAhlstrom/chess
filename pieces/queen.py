from chess.pieces import Color, Piece
from chess.pieces.movement import straight_moves, diagonal_moves


class Queen(Piece):
    """Queen piece representation.

    Moves any number of squares, straight or diagonally.
    """

    def __str__(self):
        match self.color:
            case Color.WHITE:
                return "♕"
            case Color.BLACK:
                return "♛"

    @property
    def moves(self):
        return straight_moves(self) | diagonal_moves(self)

    @property
    def value(self):
        return 9
