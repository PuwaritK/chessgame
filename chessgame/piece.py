from enum import Enum, auto
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from .board import Board


class Piece:
    def __init__(
        self, piece_type: "PieceType", color: "PieceColor", board: Board, x: int, y: int
    ) -> None:
        self.piece_type = piece_type
        self.color = color
        self.board = board
        self.posX = x
        self.posY = y


class PieceType(Enum):
    KING = auto()
    ROOK = auto()
    BISHOP = auto()
    QUEEN = auto()
    KNIGHT = auto()
    PAWN = auto()


class PieceColor(Enum):
    BLACK = auto()
    WHITE = auto()
