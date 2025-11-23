from chess.piece.color import Color
from chess.square import Coordinate
from chess.piece.pawn import Pawn
from chess.piece.knight import Knight
from chess.piece.king import King
from chess.piece.queen import Queen
from chess.piece.rook import Rook
from chess.piece.bishop import Bishop


def test_pawn_direction():
    assert Pawn(Color.WHITE).direction == -1
    assert Pawn(Color.BLACK).direction == 1


def test_pawn_moveset():
    p = Pawn(Color.WHITE)
    s = type("MockSquare", (), {"row": 6, "col": 4})()
    p.square = s
    moves = p.moves
    assert Coordinate(5, 4) in moves
    assert Coordinate(4, 4) in moves  # double push


def test_knight_moves():
    k = Knight(Color.WHITE)
    s = type("MockSquare", (), {"row": 4, "col": 4})()
    k.square = s
    assert len(k.moves) == 8
    assert all(0 <= c.row < 8 and 0 <= c.col < 8 for c in k.moves)


def test_king_moves():
    k = King(Color.WHITE)
    s = type("MockSquare", (), {"row": 4, "col": 4})()
    k.square = s
    assert len(k.moves) == 8
    assert Coordinate(5, 5) in k.moves


def test_piece_values():
    assert Pawn(Color.WHITE).value == 1
    assert Knight(Color.WHITE).value == 3
    assert Bishop(Color.WHITE).value == 3
    assert Rook(Color.WHITE).value == 5
    assert Queen(Color.WHITE).value == 9
