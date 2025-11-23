from chess.piece.color import Color
from chess.piece.rook import Rook


def test_board_starting_setup_counts(board):
    assert len(board.white_pieces) == 16
    assert len(board.black_pieces) == 16
    assert board.get_piece("e1").color == Color.WHITE
    assert board.get_piece("e8").color == Color.BLACK


def test_get_square_and_piece(board):
    sq = board.get_square("a1")
    assert sq.piece
    assert str(sq) == "a1"


def test_path_is_clear(board):
    sq1 = board.get_square("a1")
    sq2 = board.get_square("a8")
    assert not board.path_is_clear(sq1, sq2)  # blocked by pawns
    board.get_square("a2").remove_piece()
    assert not board.path_is_clear(sq1, sq2)  # still blocked further
    for r in range(1, 7):
        board.get_square((r, 0)).remove_piece()
    assert board.path_is_clear(sq1, sq2)


def test_is_square_attacked_by_rook(board):
    # Place a rook attacking a square
    from chess.piece.rook import Rook

    sq = board.get_square("e4")
    sq.add_piece(Rook(Color.WHITE))
    target = board.get_square("e7")
    assert board.is_square_attacked(target, Color.WHITE)
