from math import inf

from board import Color
from pieces import Piece
from pieces.movement import straight_moves, diagonal_moves, limit_distance


class King(Piece):
    def __str__(self):
        match self.color:
            case Color.WHITE:
                return "♔"
            case Color.BLACK:
                return "♚"

    def moves(self):
        moves = straight_moves(self) | diagonal_moves(self)
        return limit_distance(self, moves, 1)

    @property
    def value(self):
        return inf
