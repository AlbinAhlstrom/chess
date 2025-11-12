from enum import Enum


class Color(Enum):
    """Representation of piece/player color.

    Attributes:
        BLACK: Represents black pieces/player.
        WHITE: Represents white pieces/player.
    """

    BLACK = 0
    WHITE = 1


class Coordinate:
    """Represents a coordinate on a chessboard.

    Allows for row and column access as well as algebraic notation.
    Index 0 for row corresponds to the 8th rank of the board.
    Index 0 for column corresponds to the A-file.
    """

    def __init__(self, row: int, col: int):
        """Initialize a coordinate by row and column
        Attributes:
            row: Row index (0-7) => algebraic (8-1).
            col: Column index (0-7) => algebraic (A-H).
        """
        if not 0 <= row < 8:
            raise ValueError(f"Invalid row {row}")
        if not 0 <= col < 8:
            raise ValueError(f"Invalid col {col}")

        self.row = row
        self.col = col

    @property
    def algebraic_notation(self) -> str:
        """Return the squares corresponding algebraic notation."""
        return f"{chr(self.col + ord('a'))}{8 - self.row}"

    def __eq__(self, other: Coordinate) -> bool:
        """Check if two coordinates are equal.

        Args:
            other: Coordinate to compare to.

        Returns:
            bool: True if row and col attributes match, else False
        """
        return (
            isinstance(other, Coordinate)
            and self.row == other.row
            and self.col == other.col
        )

    def __repr__(self):
        return f"Coordinate({self.row}, {self.col})"

    def __hash__(self):
        return hash((self.row, self.col))

    def __str__(self):
        return self.algebraic_notation


class Board:
    """Represents the current state of a chessboard.

    Tracks the board layout, move history, player turn, castling rights,
    en passant square, and halfmove clock.
    """

    def __init__(
        self,
        board: list[list[Piece | None]],
        history: list[Board],
        player_to_move: Color,
        castling_allowed: list[Color],
        en_passant_square: Coordinate | None,
        halfmove_clock: int,
    ):
        """
        Args:
            board: 8x8 board matrix containing either Piece or None.
            history: Past board states.
            player_to_move: Piece color of the player whose turn it is.
            castling_allowed: Colors of players still allowed to castle.
            en_passant_square: Target square for en passant.
            halfmove_clock: Counter for 50-move rule.
        """
        self.board = board
        self.history = history
        self.player_to_move = player_to_move
        self.castling_allowed = castling_allowed
        self.en_passant_square = en_passant_square
        self.halfmove_clock = halfmove_clock

    @property
    def repetitions_of_position(self) -> int:
        """Count how many times the current board state has occurred.

        Used to track draw by threefold repetition.

        Returns:
            Number of repetitions of the current board position.
        """
        return sum(1 for past in self.history if past == self.board)
