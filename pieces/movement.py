from chess import Coordinate
from pieces import Piece


def straight_moves(piece: Piece):
    pos = piece.position

    horizontal_moves = {Coordinate(pos.row, col) for col in range(0, 8)}
    vertical_moves = {Coordinate(row, pos.col) for row in range(0, 8)}

    return (horizontal_moves | vertical_moves) - {Coordinate(pos.row, pos.col)}


def diagonal_moves(piece: Piece):
    pos = piece.position

    diagonal = {
        Coordinate(pos.row + offset, pos.col + offset)
        for offset in range(-7, 8)
        if 0 <= pos.row + offset < 8 and 0 <= pos.col + offset < 8
    }
    inverted_diagonal = {
        Coordinate(pos.row + offset, pos.col - offset)
        for offset in range(-7, 8)
        if 0 <= pos.row + offset < 8 and 0 <= pos.col - offset < 8
    }
    return (diagonal | inverted_diagonal) - {Coordinate(pos.row, pos.col)}
