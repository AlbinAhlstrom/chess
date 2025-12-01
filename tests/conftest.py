import pytest
from hypothesis import strategies as st

from chess.square import Square
from chess.enums import Color
from chess.piece import piece_from_char
from typing import Type


@st.composite
def rows_cols(draw):
    return draw(st.integers(min_value=0, max_value=7))


@st.composite
def squares(draw):
    return draw(st.builds(Square, row=rows_cols(), col=rows_cols()))


@st.composite
def colors(draw):
    return draw(st.sampled_from([Color.WHITE, Color.BLACK]))


piece_types: list[Type] = list(set(piece_from_char.values()))


@st.composite
def piece_types_strategy(draw):
    return draw(st.sampled_from(piece_types))


@pytest.fixture
def starting_board():
    from chess.board import Board

    return Board.starting_setup()


@st.composite
def square_notation(draw):
    """Strategy for valid chess algebraic notation (e.g., 'a1', 'h8')."""
    file_char = draw(st.sampled_from("abcdefgh"))
    rank_char = draw(st.sampled_from("12345678"))
    return file_char + rank_char
