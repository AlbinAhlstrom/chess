import pytest
from oop_chess.game import Game
from oop_chess.move import Move
from oop_chess.enums import GameOverReason, Color

def test_termination_checkmate():
    game = Game("rnb1kbnr/pppp1ppp/8/4p3/6Pq/5P2/PPPPP2P/RNBQKBNR w KQkq - 1 2")
    
    assert game.is_checkmate
    assert game.is_over
    assert game.rules.game_over_reason(game.state) == GameOverReason.CHECKMATE

def test_termination_stalemate():
    fen = "7k/5Q2/8/8/8/8/8/K7 b - - 0 1"
    game = Game(fen)
    
    assert not game.is_checkmate
    assert not game.is_check
    assert game.is_draw
    assert game.is_over
