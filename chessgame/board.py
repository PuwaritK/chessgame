import pygame
from .piece import Piece, PieceColor, PieceType, TILES_COUNT_X, TILES_COUNT_Y


class Board:
    tiles: list[list[Piece | None]]

    def __init__(self) -> None:
        self.tiles = []
        self.white_king: Piece | None = None
        self.black_king: Piece | None = None
        self.promoted_piece: Piece | None = None
        self.enpassants: list[Piece] = []
        for _ in range(TILES_COUNT_Y):
            self.tiles.append([None] * TILES_COUNT_X)

    def move_piece(self, x1: int, y1: int, x2: int, y2: int):
        moved_piece = self.get_piece(x1, y1)
        target = self.tiles[y2][x2]
        if moved_piece is None:
            raise ValueError("you tried to move nothing")

        if self._can_enpassant(moved_piece, x2, y2):
            self._enpassant(moved_piece, x2, y2)
        elif target is not None and self._can_castle(moved_piece, target):
            self._castle(moved_piece, target, x1, y1, x2, y2)
            return

        self._clear_enpassants()

        moved_piece.pos_x = x2
        moved_piece.pos_y = y2
        moved_piece.has_moved = True

        if self._can_promote(moved_piece, y2):
            self.promoted_piece = moved_piece

        self.tiles[y1][x1] = None
        self.tiles[y2][x2] = moved_piece
        self._add_enpassant(moved_piece, y1, x2, y2)
        if target is None:
            return
        if moved_piece.color == target.color:
            raise Exception("you killed your own kind")

    def get_piece(self, x: int, y: int) -> Piece | None:
        if x < 0 or y < 0:
            raise KeyError("you tried to get invalid piece")
        return self.tiles[y][x]

    def is_in_bound(self, x: int, y: int) -> bool:
        return x in range(0, TILES_COUNT_X) and y in range(0, TILES_COUNT_Y)

    def _enpassant(self, moved_piece: Piece, x2: int, y2: int):
        if moved_piece.color == PieceColor.WHITE:
            self.tiles[y2 + 1][x2] = None
        elif moved_piece.color == PieceColor.BLACK:
            self.tiles[y2 - 1][x2] = None

    def _add_enpassant(self, moved_piece: Piece, y1: int, x2: int, y2: int):
        if not abs(y2 - y1) == 2:
            return
        if moved_piece.piece_type != PieceType.PAWN:
            return

        targets: list[Piece | None] = []
        for offset_x in (-1, 1):
            if self.is_in_bound(x2 + offset_x, y2):
                targets.append(self.get_piece(x2 + offset_x, y2))

        for target in targets:
            if target is None:
                continue
            if target.piece_type != PieceType.PAWN:
                continue
            if target.color == moved_piece.color:
                continue
            if moved_piece.color == PieceColor.WHITE:
                target.enpassant = x2, y2 + 1
            elif moved_piece.color == PieceColor.BLACK:
                target.enpassant = x2, y2 - 1
            self.enpassants.append(target)

    def _castle(
        self, moved_piece: Piece, target: Piece, x1: int, y1: int, x2: int, y2: int
    ):
        if moved_piece.pos_x < target.pos_x:  # right rook
            moved_piece.pos_x = x1 + 2
            target.pos_x = x2 - 2
        else:  # left rook
            moved_piece.pos_x = x1 - 2
            target.pos_x = x2 + 3

        moved_piece.has_moved = True
        target.has_moved = True
        self.tiles[y1][x1] = None
        self.tiles[y2][x2] = None
        self.tiles[y2][moved_piece.pos_x] = moved_piece
        self.tiles[y2][target.pos_x] = target
        self._clear_enpassants()

    def _clear_enpassants(self):
        for piece in self.enpassants:
            piece.enpassant = None
        self.enpassants = []

    def _can_enpassant(self, moved_piece: Piece, x2: int, y2: int) -> bool:
        return (
            moved_piece.piece_type == PieceType.PAWN
            and moved_piece.enpassant is not None
            and moved_piece.enpassant == (x2, y2)
        )

    def _can_castle(self, moved_piece: Piece, target: Piece) -> bool:
        return (
            moved_piece.color == target.color
            and moved_piece.piece_type == PieceType.KING
            and target.piece_type == PieceType.ROOK
        )

    def _can_promote(self, moved_piece: Piece, y2: int) -> bool:
        return moved_piece.piece_type == PieceType.PAWN and (
            (y2 == 7 and moved_piece.color == PieceColor.BLACK)
            or (y2 == 0 and moved_piece.color == PieceColor.WHITE)
        )


def get_default_board() -> Board:
    board = Board()
    Piece(PieceType.ROOK, PieceColor.BLACK, board, 0, 0)
    Piece(PieceType.KNIGHT, PieceColor.BLACK, board, 1, 0)
    Piece(PieceType.BISHOP, PieceColor.BLACK, board, 2, 0)
    Piece(PieceType.QUEEN, PieceColor.BLACK, board, 3, 0)
    board.black_king = Piece(PieceType.KING, PieceColor.BLACK, board, 4, 0)
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
    board.white_king = Piece(PieceType.KING, PieceColor.WHITE, board, 4, 7)
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
