import pygame
from .piece import Piece

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
        self.tiles[x2][y2] = self.get_piece(x1, y1)
        self.tiles[x1][y1] = None

    def get_piece(self, x: int, y: int) -> Piece | None:
        if x < 0 or y < 0:
            raise KeyError("you moved the piece out of the board")
        return self.tiles[x][y]
