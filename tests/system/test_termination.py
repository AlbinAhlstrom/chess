from oop_chess.game import Game
from oop_chess.enums import GameOverReason

def test_termination_checkmate():
    game = Game("rnb1kbnr/pppp1ppp/8/4p3/6Pq/5P2/PPPPP2P/RNBQKBNR w KQkq - 1 2")

    assert game.is_checkmate
    assert game.is_over
    assert game.rules.get_game_over_reason() == GameOverReason.CHECKMATE

def test_termination_stalemate():
    fen = "7k/5Q2/8/8/8/8/8/K7 b - - 0 1"
    game = Game(fen)

    assert not game.is_checkmate
    assert game.is_over
    assert not game.is_check
    assert game.rules.get_game_over_reason() == GameOverReason.STALEMATE
    assert game.is_over
