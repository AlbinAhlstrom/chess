from hypothesis import strategies as st

from chess.square import Square
from chess.enums import Color
from chess.piece.piece import Piece
from chess.board import Board
from chess.piece import piece_from_char
from typing import Type


random_row_col = st.integers(min_value=0, max_value=7)
piece_types: list[Type[Piece]] = list(set(piece_from_char.values()))
random_color = st.sampled_from(Color)
random_piece_cls = st.sampled_from(piece_types)


@st.composite
def random_square(draw):
    return draw(st.builds(Square, row=random_row_col, col=random_row_col))


@st.composite
def random_piece(draw):
    piece_cls = draw(random_piece_cls)
    return draw(st.builds(piece_cls, color=random_color, square=st.none()))


@st.composite
def random_square_str(draw):
    file_char = draw(st.sampled_from("abcdefgh"))
    rank_char = draw(st.sampled_from("12345678"))
    return file_char + rank_char
