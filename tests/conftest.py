import pytest
from chess.board import Board
from chess.game import Game
from chess.piece.color import Color
from chess.square import Coordinate


@pytest.fixture
def board():
    return Board.starting_setup()


@pytest.fixture
def game():
    return Game()


@pytest.fixture
def white_pawn(board):
    return board.get_piece("e2")


@pytest.fixture
def black_pawn(board):
    return board.get_piece("e7")


@pytest.fixture
def coord():
    return Coordinate(4, 4)
