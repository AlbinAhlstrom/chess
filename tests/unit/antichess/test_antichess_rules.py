from v_chess.rules import AntichessRules
from v_chess.game_state import GameState
from v_chess.move import Move
from v_chess.enums import MoveLegalityReason, GameOverReason
from v_chess.game import Game

def test_mandatory_capture_simple():
    # White R at a1, Black P at a2. Capture available.
    fen = "8/8/8/8/8/8/p7/R7 w - - 0 1"
    state = GameState.from_fen(fen)
    rules = AntichessRules()
    
    # Capture is legal
    assert rules.validate_move(state, Move("a1a2")) == MoveLegalityReason.LEGAL
    
    # Non-capture (horizontal) is illegal
    assert rules.validate_move(state, Move("a1b1")) == MoveLegalityReason.MANDATORY_CAPTURE

def test_mandatory_capture_multiple_options():
    # White R b2. Black P b4, Black P d2.
    # b2b4 and b2d2 are captures.
    # b2b3 and b2c2 are non-captures.
    fen = "8/8/8/8/1p6/8/1R1p4/8 w - - 0 1"
    state = GameState.from_fen(fen)
    rules = AntichessRules()
    
    assert rules.validate_move(state, Move("b2b4")) == MoveLegalityReason.LEGAL
    assert rules.validate_move(state, Move("b2d2")) == MoveLegalityReason.LEGAL
    assert rules.validate_move(state, Move("b2b3")) == MoveLegalityReason.MANDATORY_CAPTURE
    assert rules.validate_move(state, Move("b2c2")) == MoveLegalityReason.MANDATORY_CAPTURE

def test_no_capture_allows_any_move():
    # Start pos. No captures.
    state = GameState.starting_setup()
    rules = AntichessRules()
    
    assert rules.validate_move(state, Move("e2e3")) == MoveLegalityReason.LEGAL
    assert rules.validate_move(state, Move("g1f3")) == MoveLegalityReason.LEGAL

def test_en_passant_is_mandatory():
    # White P e5. Black P d5 (just moved d7-d5). EP d6.
    # e5xd6 is capture. e5-e6 is push (non-capture).
    fen = "rnbqkbnr/ppp1pppp/8/3pP3/8/8/PPPP1PPP/RNBQKBNR w KQkq d6 0 1"
    state = GameState.from_fen(fen)
    rules = AntichessRules()
    
    assert rules.validate_move(state, Move("e5d6")) == MoveLegalityReason.LEGAL
    assert rules.validate_move(state, Move("e5e6")) == MoveLegalityReason.MANDATORY_CAPTURE

def test_king_mechanics_check_ignored():
    # King in check.
    fen = "rnb1kbnr/pppp1ppp/8/4p3/6Pq/5P2/PPPPP2P/RNBQKBNR w KQkq - 1 2"
    state = GameState.from_fen(fen)
    rules = AntichessRules()
    
    assert not rules.is_check(state)
    assert not rules.get_game_over_reason(state) == GameOverReason.CHECKMATE
    
    # King can move to attacked square?
    assert rules.validate_move(state, Move("e1f2")) == MoveLegalityReason.LEGAL

def test_castling_illegal():
    # Setup where castling would be legal in standard.
    fen = "rnbqkbnr/pppppppp/8/8/8/8/PPPPPPPP/RNBQK2R w KQkq - 0 1"
    state = GameState.from_fen(fen)
    rules = AntichessRules()
    
    # Castling e1g1
    assert rules.validate_move(state, Move("e1g1")) == MoveLegalityReason.CASTLING_DISABLED

def test_termination_zero_pieces():
    # White has no pieces.
    fen = "8/8/8/8/8/8/8/k7 w - - 0 1"
    state = GameState.from_fen(fen)
    rules = AntichessRules()
    
    assert rules.is_game_over(state)
    
def test_termination_stalemate():
    # White has pieces but no moves.
    fen = "8/8/8/8/8/p7/P7/k7 w - - 0 1"
    game = Game(fen, rules=AntichessRules())
    
    assert not game.legal_moves
    assert game.is_over
