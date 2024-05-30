import pygame
from .piece import Piece, PieceColor, PieceType

TILES_COUNT = 8


class Board:
    tiles: list[list[Piece | None]]

    def __init__(self) -> None:
        self.black_count = 16
        self.white_count = 16
        self.tiles = []
        for _ in range(TILES_COUNT):
            self.tiles.append([None] * TILES_COUNT)

    def move_piece(self, x1: int, y1: int, x2: int, y2: int):
        moved_piece = self.get_piece(x1, y1)
        if moved_piece is None:
            raise ValueError("you tried to move nothing")
        moved_piece.pos_x = x2
        moved_piece.pos_y = y2
        target = self.tiles[y2][x2]
        if target is None:
            self.tiles[y1][x1] = None
            return
        if moved_piece.color == target.color:
            raise Exception("you killed your own kind")
        if target.color == PieceColor.WHITE:
            self.white_count -= 1
        elif target.color == PieceColor.BLACK:
            self.black_count -= 1
        moved_piece.has_moved = True
        moved_piece.enpassant = None
        self.tiles[y1][x1] = None

    def get_piece(self, x: int, y: int) -> Piece | None:
        if x < 0 or y < 0:
            raise KeyError("you tried to get invalid piece")
        return self.tiles[y][x]

    def is_in_bound(self, x: int, y: int):
        return x in range(0, TILES_COUNT + 1) and y in range(0, TILES_COUNT + 1)


def get_default_board() -> Board:
    board = Board()
    Piece(PieceType.ROOK, PieceColor.BLACK, board, 0, 0)
    Piece(PieceType.KNIGHT, PieceColor.BLACK, board, 1, 0)
    Piece(PieceType.BISHOP, PieceColor.BLACK, board, 2, 0)
    Piece(PieceType.QUEEN, PieceColor.BLACK, board, 3, 0)
    Piece(PieceType.KING, PieceColor.BLACK, board, 4, 0)
    Piece(PieceType.BISHOP, PieceColor.BLACK, board, 5, 0)
    Piece(PieceType.KNIGHT, PieceColor.BLACK, board, 6, 0)
    Piece(PieceType.ROOK, PieceColor.BLACK, board, 7, 0)
    Piece(PieceType.PAWN, PieceColor.BLACK, board, 0, 1)
    Piece(PieceType.PAWN, PieceColor.BLACK, board, 1, 1)
    Piece(PieceType.PAWN, PieceColor.BLACK, board, 2, 1)
    Piece(PieceType.PAWN, PieceColor.BLACK, board, 3, 1)
    Piece(PieceType.PAWN, PieceColor.BLACK, board, 4, 1)
    Piece(PieceType.PAWN, PieceColor.BLACK, board, 5, 1)
    Piece(PieceType.PAWN, PieceColor.BLACK, board, 6, 1)
    Piece(PieceType.PAWN, PieceColor.BLACK, board, 7, 1)
    Piece(PieceType.ROOK, PieceColor.WHITE, board, 0, 7)
    Piece(PieceType.KNIGHT, PieceColor.WHITE, board, 1, 7)
    Piece(PieceType.BISHOP, PieceColor.WHITE, board, 2, 7)
    Piece(PieceType.QUEEN, PieceColor.WHITE, board, 3, 7)
    Piece(PieceType.KING, PieceColor.WHITE, board, 4, 7)
    Piece(PieceType.BISHOP, PieceColor.WHITE, board, 5, 7)
    Piece(PieceType.KNIGHT, PieceColor.WHITE, board, 6, 7)
    Piece(PieceType.ROOK, PieceColor.WHITE, board, 7, 7)
    Piece(PieceType.PAWN, PieceColor.WHITE, board, 0, 6)
    Piece(PieceType.PAWN, PieceColor.WHITE, board, 1, 6)
    Piece(PieceType.PAWN, PieceColor.WHITE, board, 2, 6)
    Piece(PieceType.PAWN, PieceColor.WHITE, board, 3, 6)
    Piece(PieceType.PAWN, PieceColor.WHITE, board, 4, 6)
    Piece(PieceType.PAWN, PieceColor.WHITE, board, 5, 6)
    Piece(PieceType.PAWN, PieceColor.WHITE, board, 6, 6)
    Piece(PieceType.PAWN, PieceColor.WHITE, board, 7, 6)
    return board
