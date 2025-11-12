from chess import Color, Coordinate
from pieces import Piece


class Knight(Piece):
    """Knight piece representation.

    Moves two squares in one direction and one square perpendicular.
    """

    def __str__(self):
        match self.color:
            case Color.WHITE:
                return "♘"
            case Color.BLACK:
                return "♞"

    def moves(self):
        pos = self.position
        offsets = (-2, -1, 1, 2)
        return {
            Coordinate(pos.row + row_offset, pos.col + column_offset)
            for row_offset in offsets
            for column_offset in offsets
            if abs(row_offset) != abs(column_offset)
            and 0 <= pos.row + row_offset < 8
            and 0 <= pos.col + column_offset < 8
        }

    @property
    def value(self):
        return 3
