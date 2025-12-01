from copy import deepcopy

from chess.board import Board
from chess.move import Move
from chess.piece.pawn import Pawn
from chess.piece.piece import Piece
from chess.enums import Color


class IllegalMoveException(Exception): ...


class Game:
    """Represents a chess game.

    Responsible for turn management.
    The majority of the game logic is handled in the Board class.
    """

    def __init__(self, board: Board):
        self.board = board
        self.history = []

    def add_to_history(self):
        self.history.append(deepcopy(self.board))

    def is_move_pseudo_legal(self, move) -> tuple[bool, str]:
        """Determine if a move is pseudolegal."""
        piece = self.board.get_piece(move.start)
        target = self.board.get_piece(move.end)

        if piece is None:
            return False, "No piece moved."

        if piece.color != self.board.player_to_move:
            return False, "Wrong piece color."

        if move.end not in piece.theoretical_moves:
            return False, "Move not in piece moveset."

        if target and target.color == self.board.player_to_move:
            return False, "Can't capture own piece."

        if isinstance(piece, Pawn):
            if move.is_vertical and target is not None:
                return False, "Cant capture forwards with pawn."

            if (
                move.is_diagonal
                and target is None
                and move.end != self.board.en_passant_square
            ):
                return False, "Diagonal pawn move requires a capture."

        if not self.board.unblocked_paths(piece):
            return False, "Path is blocked."

        return True, "Move is pseudo legal."

    @property
    def legal_moves(self) -> list[Move]:
        legal_moves = []

        for piece in self.board.current_players_pieces:
            start_square = piece.square
            if start_square is None:
                raise AttributeError("Piece has no square")

            for end_square in self.board.unblocked_paths(piece):
                move = Move(start_square, end_square)
                try:
                    if self.is_move_legal(move):
                        legal_moves.append(move)
                except IllegalMoveException:
                    pass
        return legal_moves

    @property
    def pseudo_legal_moves(self) -> list[Move]:
        # TODO: Make no check check
        legal_moves = []

        for piece in self.board.current_players_pieces:
            start_square = piece.square
            if start_square is None:
                raise AttributeError("Piece has no square")

            for end_square in self.board.unblocked_paths(piece):
                move = Move(start_square, end_square)
                try:
                    if self.is_move_legal(move):
                        legal_moves.append(move)
                except IllegalMoveException:
                    pass
        return legal_moves

    def is_move_legal(self, move: Move) -> bool:
        try:
            self.is_move_pseudo_legal(move)
        except IllegalMoveException as e:
            raise e

        if self.king_left_in_check(move):
            raise IllegalMoveException("King left in check")

        return True

    def render(self):
        """Print the board."""
        for row in range(8):
            pieces = [self.board.get_piece((row, col)) or 0 for col in range(8)]
            print(pieces)

    def king_left_in_check(self, move: Move) -> bool:
        """Returns True if king is left in check after a move."""
        real_board = self.board
        self.board = Board.from_fen(self.board.fen)

        try:
            self.board.make_move(move)

            return self.board.current_player_in_check
        finally:
            self.board = real_board

    def make_move(self, move: Move):
        """Make a move.

        Refetching board squares is necessary due to making a move
        and reverting another board object. Since move references the old
        board object new squares need to be fetched.
        """

        self.add_to_history()
        self.board.make_move(move)
        self.board.switch_active_player()
        self.increment_turn_counters(move)

    def increment_turn_counters(self, move: Move):
        piece = self.board.get_piece(move.end)
        is_pawn_move = isinstance(piece, Pawn)
        if is_pawn_move or move.is_capture:
            self.board.halfmove_clock = 0
        else:
            self.board.halfmove_clock += 1

        if self.board.player_to_move == Color.WHITE:
            self.board.fullmove_count += 1

    def undo_last_move(self) -> str:
        """Revert to the previous board state."""
        if not self.history:
            raise ValueError("No moves to undo.")

        self.board = self.history.pop()
        self.board.switch_active_player()
        return self.board.fen

    @property
    def repetitions_of_position(self) -> int:
        return sum(1 for past in self.history if past.board == self.board)
