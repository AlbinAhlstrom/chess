from enum import Enum
from abc import ABC, abstractmethod


class Color(Enum):
    BLACK = 0
    WHITE = 1


class Coordinate:
    def __init__(self, row: int, col: int):
        if not 0 <= row < 8:
            raise ValueError(f"Invalid row {row}")
        if not 0 <= col < 8:
            raise ValueError(f"Invalid col {col}")

        self.row = row
        self.col = col

    def __eq__(self, other):
        return isinstance(other, Coordinate) and self.row == other.row and self.col == other.col

    def __repr__(self):
        return f"Coordinate({self.row}, {self.col})"

    def __hash__(self):
        return hash((self.row, self.col))
    
    def __str__(self):
        return f"{chr(self.col + ord('a'))}{8 - self.row}"


class Piece(ABC):
    def __init__(self, color: Color, position: Coordinate):
        self.color = color
        self._position = position

    @property
    def position(self):
        return self._position

    @position.setter
    def position(self, position: Coordinate):
        self._position = position

    @abstractmethod
    def __str__(self):
        pass

    def __repr__(self):
        return self.__str__()


class King(Piece):
    def __str__(self):
        match self.color:
            case Color.WHITE:
                return "♔"
            case Color.BLACK:
                return "♚"


class Queen(Piece):
    def __str__(self):
        match self.color:
            case Color.WHITE:
                return "♕"
            case Color.BLACK:
                return "♛"

class Rook(Piece):
    def __str__(self):
        match self.color:
            case Color.WHITE:
                return "♖"
            case Color.BLACK:
                return "♜"


class Bishop(Piece):
    def __str__(self):
        match self.color:
            case Color.WHITE:
                return "♗"
            case Color.BLACK:
                return "♝"


class Knight(Piece):
    def __str__(self):
        match self.color:
            case Color.WHITE:
                return "♘"
            case Color.BLACK:
                return "♞"


class Pawn(Piece):
    def __str__(self):
        match self.color:
            case Color.WHITE:
                return "♙"
            case Color.BLACK:
                return "♟"


class BoardState:
    def __init__(self, board, history, player_to_move, castle_allowed, en_passant_square, turns_without_capture_or_pawn_move):
        self.board = board
        self.history = history
        self.player_to_move = player_to_move
        self.castle_allowed = castle_allowed
        self.en_passant_square = en_passant_square
        self.turns_without_capture_or_pawn_move = turns_without_capture_or_pawn_move

    @property
    def repetitions_of_position(self):
        return sum(1 for past_board in self.history if past_board == self.board)


def main():
    def setup_starting_board():
        piece_order = [Rook, Knight, Bishop, Queen, King, Bishop, Knight, Rook]

        board = [[None for _ in range(8)] for _ in range(8)]

        board[0] = [piece(Color.BLACK, Coordinate(0, col)) for col, piece in enumerate(piece_order)]
        board[1] = [Pawn(Color.BLACK, Coordinate(1, col)) for col in range(8)]

        board[6] = [Pawn(Color.WHITE, Coordinate(6, col)) for col in range(8)]
        board[7] = [piece(Color.WHITE, Coordinate(7, col)) for col, piece in enumerate(piece_order)]

        return board

    board = setup_starting_board()
    history = [board]
    player_to_move = Color.WHITE
    castle_allowed = [Color.WHITE, Color.BLACK]
    en_passant_square = None
    turns_without_capture_or_pawn_move = 0

    state = BoardState(board, history, player_to_move, castle_allowed, en_passant_square, turns_without_capture_or_pawn_move)
    for row in state.board:
        row = [char or 0 for char in row]
        print(row)

if __name__ == "__main__":
    main()

