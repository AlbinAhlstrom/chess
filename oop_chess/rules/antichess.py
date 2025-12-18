from oop_chess.enums import Color, MoveLegalityReason, StatusReason, GameOverReason
from oop_chess.move import Move
from oop_chess.piece import King, Pawn
from oop_chess.game_state import GameState
from .standard import StandardRules


class AntichessRules(StandardRules):
    @property
    def name(self) -> str:
        return "Antichess"

    @property
    def has_check(self) -> bool:
        return False

    def validate_move(self, state: GameState, move: Move) -> MoveLegalityReason:
        pseudo_reason = self.move_pseudo_legality_reason(state, move)
        if pseudo_reason != MoveLegalityReason.LEGAL:
            return pseudo_reason

        if self._is_capture(state, move):
            return MoveLegalityReason.LEGAL

        # If move is not a capture, ensure no captures are available
        for opt_move in self.get_theoretical_moves(state):
            if self.move_pseudo_legality_reason(state, opt_move) == MoveLegalityReason.LEGAL:
                if self._is_capture(state, opt_move):
                    return MoveLegalityReason.MANDATORY_CAPTURE
        return MoveLegalityReason.LEGAL

    def _is_capture(self, state: GameState, move: Move) -> bool:
        if state.board.get_piece(move.end):
            return True
        piece = state.board.get_piece(move.start)
        if isinstance(piece, Pawn) and move.end == state.ep_square:
            return True
        return False

    def is_check(self, state: GameState) -> bool:
        return False

    def inactive_player_in_check(self, state: GameState) -> bool:
        return False

    def get_game_over_reason(self, state: GameState) -> GameOverReason:
        if not state.board.get_pieces(color=state.turn):
            return GameOverReason.ALL_PIECES_CAPTURED
        if not self.get_legal_moves(state):
             return GameOverReason.STALEMATE
        return GameOverReason.ONGOING

    def validate_board_state(self, state: GameState) -> StatusReason:
        white_pawns = state.board.get_pieces(Pawn, Color.WHITE)
        black_pawns = state.board.get_pieces(Pawn, Color.BLACK)
        pawns_on_backrank = []
        for sq, piece in state.board.board.items():
             if isinstance(piece, Pawn) and (sq.row == 0 or sq.row == 7):
                 pawns_on_backrank.append(piece)

        is_ep_square_valid = state.ep_square is None or state.ep_square.row in (2, 5)

        if len(white_pawns) > 8:
            return StatusReason.TOO_MANY_WHITE_PAWNS
        if len(black_pawns) > 8:
            return StatusReason.TOO_MANY_BLACK_PAWNS
        if pawns_on_backrank:
            return StatusReason.PAWNS_ON_BACKRANK

        if not is_ep_square_valid:
            return StatusReason.INVALID_EP_SQUARE

        return StatusReason.VALID

    def get_winner(self, state: GameState) -> Color | None:
        reason = self.get_game_over_reason(state)
        if reason in (GameOverReason.ALL_PIECES_CAPTURED, GameOverReason.STALEMATE):
             return state.turn
        return None

    def castling_legality_reason(self, state: GameState, move: Move, piece: King) -> MoveLegalityReason:
        return MoveLegalityReason.CASTLING_DISABLED

    def get_legal_castling_moves(self, state: GameState) -> list[Move]:
        return []
