from math import inf

from chess.piece.piece import Piece
from chess.enums import Color, Moveset


class King(Piece):
    """King piece representation.

    Moves one square in any direction.
    Special rules for castling and check are implemented in Board.legal_move.
    """

    MOVESET = Moveset.STRAIGHT_AND_DIAGONAL

    @property
    def theoretical_moves(self):
        if self.square is None:
            raise AttributeError("Can't get moves for a piece with no square.")

        return [self.square.get_adjacent(direction) for direction in self.MOVESET.value]

    def __str__(self):
        match self.color:
            case Color.WHITE:
                return "♔"
            case Color.BLACK:
                return "♚"

    @property
    def value(self):
        return inf

    @property
    def fen(self):
        return "K" if self.color == Color.WHITE else "k"
