from oop_chess.game import Game
from oop_chess.rules import AntichessRules
from oop_chess.board import Board
from oop_chess.piece import Pawn, Rook, King
from oop_chess.square import Square
from oop_chess.enums import Color
from oop_chess.move import Move

def test_mandatory_capture():
    # White pawn at e4, Black pawn at d5. White to move.
    # Capture e4xd5 is mandatory. e4-e5 is illegal.
    
    fen = "8/8/8/3p4/4P3/8/8/8 w - - 0 1"
    game = Game(fen=fen, rules=AntichessRules())
    
    legal_moves = game.legal_moves
    assert len(legal_moves) == 1
    assert legal_moves[0].uci == "e4d5"

def test_multiple_captures_mandatory():
    # White Rook at a1. Black pawns at a2, b1.
    # Captures: a1xa2, a1xb1.
    # Non-capture: None (Rook blocked).
    # Put Black pawn at b2 (attacked).
    
    # White Rook a1. Black Pawn a5. Black Pawn h1.
    # a1xa5 is capture. a1xh1 is capture.
    # a1-a2...a4 non-captures.
    
    fen = "8/8/8/p7/8/8/8/R6p w - - 0 1"
    game = Game(fen=fen, rules=AntichessRules())
    
    captures = [m.uci for m in game.legal_moves]
    assert "a1a5" in captures
    assert "a1h1" in captures
    assert "a1a2" not in captures

def test_king_can_move_into_check():
    # White King at e1, Black Rook at e8.
    # e1-e2 is legal even though attacked.
    
    fen = "4r3/8/8/8/8/8/8/4K3 w - - 0 1"
    game = Game(fen=fen, rules=AntichessRules())
    
    # Check is false
    assert not game.is_check
    
    legal_moves = [m.uci for m in game.legal_moves]
    assert "e1e2" in legal_moves
    assert "e1f1" in legal_moves # etc.

def test_game_over_no_pieces():
    # White has no pieces. White wins (game over).
    fen = "8/8/8/8/8/8/8/k7 w - - 0 1" # White to move but no pieces
    
    game = Game(fen=fen, rules=AntichessRules())
    assert game.is_over


