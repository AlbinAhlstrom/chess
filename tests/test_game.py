from chess.piece.color import Color
from chess.piece.pawn import Pawn
from chess.square import Square, Coordinate
from chess.move import Move


def test_turn_switching(game):
    assert game.current_player == Color.WHITE
    game.switch_current_player()
    assert game.current_player == Color.BLACK


def test_make_move_switches_turn(game):
    start = game.board.get_square("e2")
    end = game.board.get_square("e4")
    move = game.board.get_move(start, end)
    assert game.move_is_legal(move)
    game.make_move(move)
    assert game.current_player == Color.BLACK


def test_undo_last_move_restores_board(game):
    start = game.board.get_square("e2")
    end = game.board.get_square("e4")
    move = game.board.get_move(start, end)
    game.make_move(move)
    game.undo_last_move()
    assert game.board.get_piece("e2").__class__.__name__ == "Pawn"


def test_cannot_move_opponents_piece(game):
    move = game.board.get_move(game.board.get_square("e7"), game.board.get_square("e5"))
    assert not game.move_is_legal(move)


def test_pawn_capture_legality(game):
    # Set up quick scenario
    e2 = game.board.get_square("e2")
    e4 = game.board.get_square("e4")
    e2.piece = e4.piece
    e4.piece = None
    move = game.board.get_move(e2, e4)
    assert not game.move_is_legal(move)


def test_castling_rules(game):
    board = game.board
    # Clear path for white king
    for c in [5, 6]:
        board.get_square((7, c)).remove_piece()
    assert board.short_castle_allowed
    board.short_castle()
    king_square = board.get_square("g1")
    rook_square = board.get_square("f1")
    assert str(king_square.piece) == "♔"


def test_en_passant_square_set_after_double_push(game):
    start = game.board.get_square("e2")
    end = game.board.get_square("e4")
    move = game.board.get_move(start, end)
    game.make_move(move)
    assert str(game.board.en_passant_square) == "e3"


def test_checkmate_and_draw_detection(game):
    # A starting position should be neither
    assert not game.is_checkmate
    assert not game.is_draw
    rook_square = game.board.get_square("a1")
    assert str(rook_square.piece) == "♖"
