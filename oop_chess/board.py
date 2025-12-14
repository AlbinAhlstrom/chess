from typing import TypeVar

from oop_chess.piece import piece_from_char
from oop_chess.enums import Color
from oop_chess.piece.piece import Piece
from oop_chess.square import Coordinate, Square


T = TypeVar("T", bound=Piece)


class Board:
    """Represents the spatial configuration of pieces (The Database).

    It answers queries about piece locations and paths.
    It does NOT know about game state (turn, castling rights, etc.).
    """
    STARTING_POSITION = "rnbqkbnr/pppppppp/8/8/8/8/PPPPPPPP/RNBQKBNR"

    def __init__(self, pieces: dict[Square, Piece] = {}):
        self.board: dict[Square, Piece] = pieces if pieces else {}

    def get_piece(self, coordinate: Coordinate) -> Piece | None:
        return self.board.get(Square.from_coord(coordinate))

    def set_piece(self, piece: Piece, square: str | tuple | Square):
        square = Square.from_coord(square)
        self.board[square] = piece

    def remove_piece(self, coordinate: Coordinate) -> Piece | None:
        square = Square.from_coord(coordinate)
        return self.board.pop(square, None)

    def move_piece(self, piece: Piece, start: Square, end: Square):
        """Moves a piece on the board. Does not handle capture logic or rules."""
        self.set_piece(piece, end)
        self.remove_piece(start)

    def get_pieces(
        self, piece_type: type[T] = Piece, color: Color | None = None
    ) -> list[T]:
        pieces = [piece for piece in self.board.values() if piece]
        pieces = [piece for piece in pieces if isinstance(piece, piece_type)]
        if color is not None:
            pieces = [piece for piece in pieces if piece.color.value == color.value]
        return pieces

    @classmethod
    def empty(cls) -> "Board":
        return cls()

    @classmethod
    def starting_setup(cls) -> "Board":
        return cls.from_fen(cls.STARTING_POSITION)

    @classmethod
    def from_fen(cls, fen_board: str) -> "Board":
        """Parses the piece placement part of a FEN string."""
        board: dict[Square, Piece] = {}
        fen_rows = fen_board.split("/")
        for row, fen_row in enumerate(fen_rows):
            empty_squares = 0
            for col, char in enumerate(fen_row):
                if char.isdigit():
                    empty_squares += int(char) - 1
                else:
                    is_white = char.isupper()
                    piece_color = Color.WHITE if is_white else Color.BLACK
                    piece_type = piece_from_char.get(char)
                    if piece_type is None:
                        raise ValueError(f"Invalid piece in FEN: {char}")
                    piece = piece_type(piece_color)
                    coord = Square(row, col + empty_squares)
                    board[coord] = piece
        return cls(board)

    def _get_fen_row(self, row) -> str:
        empty_squares = 0
        fen_row_string = ""
        for col in range(8):
            coord = Square(row, col)
            piece = self.board.get(coord)

            if piece is None:
                empty_squares += 1
                continue

            if empty_squares > 0:
                fen_row_string += str(empty_squares)
                empty_squares = 0

            fen_row_string += piece.fen

        if empty_squares > 0:
            fen_row_string += str(empty_squares)
        return fen_row_string

    @property
    def fen(self) -> str:
        """Generates the piece placement part of FEN."""
        fen_rows = (self._get_fen_row(row) for row in range(8))
        return "/".join(fen_rows)

    def __str__(self):

        return self.fen

    def copy(self) -> "Board":
        return Board(self.board.copy())

