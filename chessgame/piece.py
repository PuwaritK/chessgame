from enum import Enum, auto
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from .board import Board


class Piece:
    def __init__(
        self,
        piece_type: "PieceType",
        color: "PieceColor",
        board: Board,
        x: int,
        y: int,
    ) -> None:
        self.piece_type = piece_type
        self.color = color
        self.board = board
        self.posX = x
        self.posY = y

    def available_moves(self) -> list[tuple[int, int]]:
        possible_tiles = []
        match self.piece_type:
            case PieceType.KING:
                for x in range(-1, 2):
                    for y in range(-1, 2):
                        if x == 0 and y == 0:
                            continue
                        if not self.board.is_in_bound(self.posX + x, self.posY + y):
                            continue
                        if self.is_ally(x, y):
                            continue
                        possible_tiles.append((x + self.posX, y + self.posY))

            case PieceType.ROOK:
                for offset in range(0, 8):  # east
                    if not self.board.is_in_bound(self.posX + offset, self.posY):
                        break
                    if self.is_ally(self.posX + offset, self.posY):
                        break
                    possible_tiles.append((offset + self.posX, self.posY))
                    if self.is_enemy(self.posX + offset, self.posY):
                        break

                for offset in range(0, 8):  # west
                    if not self.board.is_in_bound(self.posX - offset, self.posY):
                        break
                    if self.is_ally(self.posX - offset, self.posY):
                        break
                    possible_tiles.append((offset - self.posX, self.posY))
                    if self.is_enemy(self.posX - offset, self.posY):
                        break

                for offset in range(0, 8):  # north
                    if not self.board.is_in_bound(self.posX, self.posY + offset):
                        break
                    if self.is_ally(self.posX, self.posY + offset):
                        break
                    possible_tiles.append((self.posX, self.posY + offset))
                    if self.is_enemy(self.posX, self.posY + offset):
                        break

                for offset in range(0, 8):  # south
                    if not self.board.is_in_bound(self.posX, self.posY - offset):
                        break
                    if self.is_ally(self.posX, self.posY - offset):
                        break
                    possible_tiles.append((self.posX, self.posY - offset))
                    if self.is_enemy(self.posX, self.posY - offset):
                        break
            case PieceType.QUEEN:
                pass
            case PieceType.BISHOP:
                pass
            case PieceType.KNIGHT:
                pass
            case PieceType.PAWN:
                pass
        return possible_tiles

    def is_ally(self, x: int, y: int):
        them = self.board.get_piece(x, y)
        if them is not None:
            return them.color == self.color
        return False

    def is_enemy(self, x: int, y: int):
        them = self.board.get_piece(x, y)
        if them is not None:
            return them.color != self.color
        return False


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
