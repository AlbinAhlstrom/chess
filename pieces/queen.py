from board import Color
from pieces import Piece
from pieces.movement import straight_moves, diagonal_moves


class Queen(Piece):
    def __str__(self):
        match self.color:
            case Color.WHITE:
                return "♕"
            case Color.BLACK:
                return "♛"

    def moves(self):
        return straight_moves(self) | diagonal_moves(self)

    @property
    def value(self):
        return 9
