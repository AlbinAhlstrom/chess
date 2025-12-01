from hypothesis import given
from math import inf
from typing import Type

from chess.piece.piece import Piece
from chess.enums import Color
from conftest import piece_types_strategy, colors


@given(piece_type=piece_types_strategy(), color=colors())
def test_piece_fen_is_correct_case(piece_type: Type[Piece], color: Color):
    """
    Checks that the FEN representation (piece.fen) is uppercase for WHITE
    and lowercase for BLACK, and that it is a single character.
    """
    piece = piece_type(color)
    fen_char = piece.fen

    assert len(fen_char) == 1

    if color == Color.WHITE:
        assert fen_char.isupper()
    else:
        assert fen_char.islower()


@given(piece_type=piece_types_strategy(), color=colors())
def test_piece_has_valid_value(piece_type: Type[Piece], color: Color):
    """
    Checks that all pieces have a non-negative value.
    """
    piece = piece_type(color)
    value = piece.value

    assert value >= 0

    if piece_type.__name__ != "King":
        assert value != inf
        assert isinstance(value, int)
    else:
        assert value == inf
