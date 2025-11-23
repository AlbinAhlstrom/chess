from chess.move import Move
from chess.piece.pawn import Pawn
from chess.square import Square
from chess.piece.color import Color


def test_move_flags(board):
    start = board.get_square("e2")
    end = board.get_square("e4")
    move = board.get_move(start, end)
    assert move.is_double_pawn_push
    assert not move.is_capture
    assert not move.is_en_passant
