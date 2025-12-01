from hypothesis import given

from chess.board import Board
from chess.square import Square
from chess.piece import Piece
from chess.piece.pawn import Pawn
from chess.enums import Color
from conftest import random_square, random_piece


@given(square=random_square(), piece=random_piece())
def test_pawn_two_step_move(square: Square, piece: Piece):
    """
    Specific check: For an un-moved pawn, ensure the double-step square is included
    in theoretical moves if it's a valid square.
    """
    board = Board.empty()
    board.set_piece(piece, square)
    if not isinstance(piece, Pawn):
        return

    piece.has_moved = False
    start_square = piece.square
    assert start_square is not None

    single_step = start_square.get_step(piece.direction)
    double_step = single_step.get_step(piece.direction) if single_step else None

    theoretical_moves = piece.theoretical_moves

    if double_step:
        assert double_step in theoretical_moves

@given(square=random_square(), piece=random_piece())
def test_pawn_capture(square: Square, piece: Piece):
    board = Board.empty()
    board.set_piece(piece, square)

    assert piece.square is not None

    if not isinstance(piece, Pawn):
        return

    last_row = 0 if piece.color == Color.WHITE else 7
    is_on_last_row = square.row == last_row
    is_on_edge = square.col in (0, 7)

    if is_on_last_row:
        return

    expected_captures= 2
    if square.col in (0, 7):
        expected_captures = 1

    assert len(piece.capture_squares) == expacted_captures, f"{expected_captures=} got {piece.capture_squares} for {piece.color} pawn at {square}"



