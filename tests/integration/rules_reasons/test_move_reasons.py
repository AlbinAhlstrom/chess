import pytest
from oop_chess.game_state import GameState
from oop_chess.rules import StandardRules
from oop_chess.enums import MoveLegalityReason, Color
from oop_chess.move import Move
from oop_chess.piece import Queen

def test_reason_no_piece():
    rules = StandardRules()
    state = GameState.starting_setup()
    move = Move("e3e4")
    assert rules.move_legality_reason(state, move) == MoveLegalityReason.NO_PIECE

def test_reason_wrong_color():
    rules = StandardRules()
    state = GameState.starting_setup()
    move = Move("e7e5")
    assert rules.move_legality_reason(state, move) == MoveLegalityReason.WRONG_COLOR

def test_reason_no_castling_right():
    rules = StandardRules()
    fen = "r3k2r/8/8/8/8/8/8/R3K2R w - - 0 1"
    state = GameState.from_fen(fen)
    move = Move("e1g1")
    assert rules.move_legality_reason(state, move) == MoveLegalityReason.NO_CASTLING_RIGHT

def test_reason_castling_from_check():
    rules = StandardRules()
    fen = "r3k2r/8/8/8/8/8/4r3/R3K2R w KQkq - 0 1"
    state = GameState.from_fen(fen)
    move = Move("e1g1")
    assert rules.move_legality_reason(state, move) == MoveLegalityReason.CASTLING_FROM_CHECK

def test_reason_castling_through_check():
    rules = StandardRules()
    fen = "r3k2r/8/8/8/8/8/5r2/R3K2R w KQkq - 0 1"
    state = GameState.from_fen(fen)
    move = Move("e1g1")
    assert rules.move_legality_reason(state, move) == MoveLegalityReason.CASTLING_THROUGH_CHECK

def test_reason_not_in_moveset():
    rules = StandardRules()
    state = GameState.starting_setup()
    move = Move("e2e5")
    assert rules.move_legality_reason(state, move) == MoveLegalityReason.NOT_IN_MOVESET

def test_reason_own_piece_capture():
    rules = StandardRules()
    state = GameState.starting_setup()
    move = Move("a1a2")
    assert rules.move_legality_reason(state, move) == MoveLegalityReason.OWN_PIECE_CAPTURE

def test_reason_forward_pawn_capture():
    rules = StandardRules()
    fen = "8/8/8/8/4p3/4P3/8/8 w - - 0 1"
    state = GameState.from_fen(fen)
    move = Move("e3e4")
    assert rules.move_legality_reason(state, move) == MoveLegalityReason.FORWARD_PAWN_CAPTURE

def test_reason_pawn_diagonal_non_capture():
    rules = StandardRules()
    state = GameState.starting_setup()
    move = Move("e2f3")
    assert rules.move_legality_reason(state, move) == MoveLegalityReason.PAWN_DIAGONAL_NON_CAPTURE

def test_reason_non_promotion():
    rules = StandardRules()
    fen = "8/P7/8/8/8/8/8/8 w - - 0 1"
    state = GameState.from_fen(fen)
    move = Move("a7a8")
    assert rules.move_legality_reason(state, move) == MoveLegalityReason.NON_PROMOTION

def test_reason_path_blocked():
    rules = StandardRules()
    state = GameState.starting_setup()
    move = Move("a1a3")
    assert rules.move_legality_reason(state, move) == MoveLegalityReason.PATH_BLOCKED

from oop_chess.square import Square

def test_reason_early_promotion():
    rules = StandardRules()
    state = GameState.starting_setup()
    move = Move(Square("e2"), Square("e3"), Queen(Color.WHITE))
    assert rules.move_legality_reason(state, move) == MoveLegalityReason.EARLY_PROMOTION

def test_reason_king_left_in_check():
    rules = StandardRules()
    fen = "rnbqkbnr/pppp1Qpp/8/4p3/4P3/8/PPPP1PPP/RNB1KBNR b KQkq - 0 1"
    state = GameState.from_fen(fen)
    move = Move("a7a6")
    assert rules.move_legality_reason(state, move) == MoveLegalityReason.KING_LEFT_IN_CHECK
