from abc import ABC, abstractmethod

from oop_chess.board import Board
from oop_chess.enums import StatusReason
from oop_chess.move import Move
from oop_chess.piece.knight import Knight


class Rules(ABC):
    @abstractmethod
    def get_legal_moves(self, board: Board) -> list[Move]: ...

    @abstractmethod
    def is_check(self, board: Board) -> list[Move]: ...

    @abstractmethod
    def is_game_over(self, board: Board) -> list[Move]: ...


class StandardRules:
    def is_attacking(self, piece, square, board):
        if isinstance(piece, (Pawn, King, Knight)):
            return square in piece.capture_squares
        else:
            return square in self.unblocked_paths(piece)

    def is_under_attack(self, square: Square, by_color: Color) -> bool:
        """Check if square is attacked by the given color."""
        attackers = self.get_pieces(color=by_color)
        return any([self.is_attacking(piece, square) for piece in attackers])

    def player_in_check(self, color: Color) -> bool:
        king = self.get_pieces(King, color)[0]
        if king.square is None:
            raise AttributeError("King not found on board.")
        return self.is_under_attack(king.square, color.opposite)
    @property
    def is_board_state_legal(self, board: Board) -> bool:
        return self.status == StatusReason.VALID

    @property
    def status(self, board: Board) -> StatusReason:
        """Return True if board state is legal."""
        white_kings = self.get_pieces(King, Color.WHITE)
        black_kings = self.get_pieces(King, Color.BLACK)
        white_pawns = self.get_pieces(Pawn, Color.WHITE)
        black_pawns = self.get_pieces(Pawn, Color.BLACK)
        white_non_pawns = [piece for piece in self.get_pieces(color=Color.WHITE) if not isinstance(piece, Pawn)]
        black_non_pawns = [piece for piece in self.get_pieces(color=Color.BLACK) if not isinstance(piece, Pawn)]
        white_piece_max = 16 - len(white_pawns)
        black_piece_max = 16 - len(black_pawns)
        pawns_on_backrank = [piece for piece in self.get_pieces(Pawn) if piece.is_on_first_or_last_row]
        print([str(p) for p in pawns_on_backrank])
        is_ep_square_valid = self.ep_square is None or self.ep_square.row in (2, 5)

        if len(white_kings) < 1:
            return StatusReason.NO_WHITE_KING
        if len(black_kings) < 1:
            return StatusReason.NO_BLACK_KING
        if len(white_kings + black_kings) > 2:
            return StatusReason.TOO_MANY_KINGS

        if len(white_pawns) > 8:
            return StatusReason.TOO_MANY_WHITE_PAWNS
        if len(black_pawns) > 8:
            return StatusReason.TOO_MANY_BLACK_PAWNS
        if pawns_on_backrank:
            return StatusReason.PAWNS_ON_BACKRANK

        if len(white_non_pawns) > white_piece_max:
            return StatusReason.TOO_MANY_WHITE_PIECES
        if len(black_non_pawns) > black_piece_max:
            return StatusReason.TOO_MANY_BLACK_PIECES

        if self.invalid_castling_rights:
            return StatusReason.INVALID_EP_SQUARE

        if not is_ep_square_valid:
            return StatusReason.INVALID_EP_SQUARE

        if self.inactive_player_in_check:
            return StatusReason.OPPOSITE_CHECK

        return StatusReason.VALID
