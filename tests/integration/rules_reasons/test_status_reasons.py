import pytest
from oop_chess.game_state import GameState
from oop_chess.rules import StandardRules
from oop_chess.enums import StatusReason

def test_status_reason_valid():
    rules = StandardRules()
    state = GameState.starting_setup()
    assert rules.status(state) == StatusReason.VALID

def test_status_reason_no_white_king():
    rules = StandardRules()
    fen = "rnbqkbnr/pppppppp/8/8/8/8/PPPPPPPP/RNBQ1BNR w KQkq - 0 1"
    state = GameState.from_fen(fen)
    assert rules.status(state) == StatusReason.NO_WHITE_KING

def test_status_reason_no_black_king():
    rules = StandardRules()
    fen = "rnbq1bnr/pppppppp/8/8/8/8/PPPPPPPP/RNBQKBNR w KQkq - 0 1"
    state = GameState.from_fen(fen)
    assert rules.status(state) == StatusReason.NO_BLACK_KING

def test_status_reason_too_many_kings():
    rules = StandardRules()
    fen = "rnbqkbnr/pppppppp/8/8/8/8/PPPPPPPP/RNBQKBNK w KQkq - 0 1"
    state = GameState.from_fen(fen)
    assert rules.status(state) == StatusReason.TOO_MANY_KINGS

def test_status_reason_too_many_white_pawns():
    rules = StandardRules()
    fen = "rnbqkbnr/pppppppp/8/8/P7/8/PPPPPPPP/RNBQKBNR w KQkq - 0 1"
    state = GameState.from_fen(fen)
    assert rules.status(state) == StatusReason.TOO_MANY_WHITE_PAWNS

def test_status_reason_too_many_black_pawns():
    rules = StandardRules()
    fen = "rnbqkbnr/pppppppp/8/p7/8/8/PPPPPPPP/RNBQKBNR w KQkq - 0 1"
    state = GameState.from_fen(fen)
    assert rules.status(state) == StatusReason.TOO_MANY_BLACK_PAWNS

def test_status_reason_pawns_on_backrank():
    rules = StandardRules()
    fen = "rnbqkbnr/pppppppp/8/8/8/8/8/PNBQKBNR w KQkq - 0 1"
    state = GameState.from_fen(fen)
    assert rules.status(state) == StatusReason.PAWNS_ON_BACKRANK

def test_status_reason_too_many_white_pieces():
    rules = StandardRules()
    fen = "RQBQQBNR/8/8/3Q4/4Q3/8/8/RNBQKBNk w KQkq - 0 1"
    state = GameState.from_fen(fen)
    assert rules.status(state) == StatusReason.TOO_MANY_WHITE_PIECES

def test_status_reason_too_many_black_pieces():
    rules = StandardRules()
    fen = "rnbqkbnr/8/8/3q4/4q3/8/8/rnbqqbnK w KQkq - 0 1"
    state = GameState.from_fen(fen)
    assert rules.status(state) == StatusReason.TOO_MANY_BLACK_PIECES

def test_status_reason_invalid_castling_rights_king_missing():
    rules = StandardRules()
    fen = "rnbqkbnr/pppppppp/8/8/8/4K3/PPPPPPPP/RNBQ1BNR w K - 0 1"
    state = GameState.from_fen(fen)
    assert rules.status(state) == StatusReason.INVALID_CASTLING_RIGHTS

def test_status_reason_invalid_castling_rights_rook_missing():
    rules = StandardRules()
    fen = "1nbqkbnr/pppppppp/8/8/8/8/PPPPPPPP/RNBQKBNR w q - 0 1"
    state = GameState.from_fen(fen)
    assert rules.status(state) == StatusReason.INVALID_CASTLING_RIGHTS

def test_status_reason_invalid_ep_square():
    rules = StandardRules()
    fen = "rnbqkbnr/pppppppp/8/8/8/8/PPPPPPPP/RNBQKBNR w KQkq e4 0 1"
    state = GameState.from_fen(fen)
    assert rules.status(state) == StatusReason.INVALID_EP_SQUARE

def test_status_reason_opposite_check():
    rules = StandardRules()
    fen = "rnbq1bnr/pppppppp/8/8/8/4k3/PPPPQPPP/RNB1KBNR w KQ - 0 1"
    state = GameState.from_fen(fen)
    assert rules.status(state) == StatusReason.OPPOSITE_CHECK
