from hypothesis import given
from math import inf

from chess.piece.bishop import Bishop
from chess.piece.king import King
from chess.piece.knight import Knight
from chess.piece.pawn import Pawn
from chess.piece.piece import Piece
from chess.enums import Color
from chess.board import Board
from chess.piece.queen import Queen
from chess.piece.rook import Rook
from chess.square import Square
from conftest import random_square, random_piece


@given(piece=random_piece())
def test_piece_fen_is_correct_case(piece: Piece):
    """
    Checks that the FEN representation (piece.fen) is uppercase for WHITE
    and lowercase for BLACK, and that it is a single character.
    """
    fen_char = piece.fen

    assert len(fen_char) == 1

    if piece.color == Color.WHITE:
        assert fen_char.isupper()
    else:
        assert fen_char.islower()


@given(piece=random_piece())
def test_piece_has_valid_value(piece: Piece):
    """
    Checks that all pieces have a non-negative value.
    """
    value = piece.value

    assert value >= 0

    if piece.__class__.__name__ != "King":
        assert value != inf
        assert isinstance(value, int)
    else:
        assert value == inf
