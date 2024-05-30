import pygame
from .piece import Piece, PieceColor

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
        target = self.tiles[x2][y2]
        if target is None:
            self.tiles[x1][y1] = None
            return
        if moved_piece.color == target.color:
            raise Exception("you killed your own kind")
        if target.color == PieceColor.WHITE:
            self.white_count -= 1
        elif target.color == PieceColor.BLACK:
            self.black_count -= 1
        moved_piece.has_moved = True
        moved_piece.enpassant = None
        self.tiles[x1][y1] = None

    def get_piece(self, x: int, y: int) -> Piece | None:
        if x < 0 or y < 0:
            raise KeyError("you tried to get invalid piece")
        return self.tiles[x][y]

    def is_in_bound(self, x: int, y: int):
        return x in range(0, TILES_COUNT + 1) and y in range(0, TILES_COUNT + 1)
