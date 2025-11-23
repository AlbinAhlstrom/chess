from dataclasses import dataclass, field

from chess.square import Square
from chess.piece.pawn import Pawn


@dataclass(frozen=True)
class Move:
    start: Square
    end: Square
    piece: Piece
    target_piece: Optional[Piece]
    promotion_piece: Piece = None
    is_castling: bool = False

    @property
    def is_promotion(self) -> bool:
        return self.promotion_piece is not None

    @property
    def is_capture(self) -> bool:
        return self.piece_captured is not None or self.is_en_passant

    @property
    def is_double_pawn_push(self) -> bool:
        from chess.piece.piece import Piece

        return isinstance(self.piece, Pawn) and abs(self.start.row - self.end.row) == 2

    @property
    def is_en_passant(self) -> bool:
        from chess.piece.piece import Piece

        return (
            isinstance(self.piece, Pawn)
            and self.target_piece is None
            and self.start.col != self.end.col
        )
