from string import ascii_lowercase

from chess.pieces import Rook, Knight, Bishop, Queen, King, Pawn, Color
from chess.square import Square
from chess.move import Move


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
        en_passant_square: Square | None,
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
        self.pieces = [
            piece for row in self.board for piece in row if piece is not None
        ]

    @classmethod
    def starting_setup(cls) -> Board:
        """Return a list of lists representing the starting chess board.

        Returns:
            8x8 board with pieces in standard starting positions.
        """
        pieces = [Rook, Knight, Bishop, Queen, King, Bishop, Knight, Rook]
        board = [[Square((row, col)) for row in rows] for col in cols]

        for b_square, w_square, piece in zip(board[0], board[6], pieces):
            b_square.add_piece(piece(Color.BLACK))
            w_square.add_piece(piece(Color.WHITE))

        for b_square, w_square, piece in zip(board[1], board[7]):
            b_square.add_piece(Pawn(Color.BLACK))
            w_square.add_piece(Pawn(Color.WHITE))

        return cls(
            board=board,
            history=[board.copy()],
            player_to_move=Color.WHITE,
            castling_allowed=[Color.WHITE, Color.BLACK],
            en_passant_square=None,
            halfmove_clock=0,
        )

    def move_piece(self, move):
        pass

    @property
    def repetitions_of_position(self) -> int:
        """Count how many times the current board state has occurred.

        Used to track draw by threefold repetition.

        Returns:
            Number of repetitions of the current board position.
        """
        return sum(1 for past in self.history if past == self.board)
