from enum import Enum, auto
from typing import TYPE_CHECKING, Iterable
from itertools import repeat

if TYPE_CHECKING:
    from .board import Board

TILES_COUNT_X = 8
TILES_COUNT_Y = 8


def get_nsew():
    return (
        zip(repeat(0), range(-1, -TILES_COUNT_Y, -1)),  # north
        zip(repeat(0), range(1, TILES_COUNT_Y)),  # south
        zip(range(1, TILES_COUNT_X), repeat(0)),  # east
        zip(range(-1, -TILES_COUNT_X, -1), repeat(0)),  # west
    )


def get_diagonals():
    return (
        zip(range(1, TILES_COUNT_X), range(-1, -TILES_COUNT_Y, -1)),  # north east
        zip(range(1, TILES_COUNT_X), range(1, TILES_COUNT_Y)),  # south east
        zip(range(-1, -TILES_COUNT_X, -1), range(-1, -TILES_COUNT_Y, -1)),  # north west
        zip(range(-1, -TILES_COUNT_X, -1), range(1, TILES_COUNT_Y)),  # south west)
    )


def king_castle_tiles():
    return (
        zip(range(1, TILES_COUNT_X), repeat(0)),  # east
        zip(range(-1, -TILES_COUNT_X, -1), repeat(0)),  # west
    )


KNIGHT_OFFSETS = (
    (-2, -1),
    (-1, -2),
    (1, -2),
    (2, -1),
    (2, 1),
    (1, 2),
    (-1, 2),
    (-2, 1),
)


class Piece:
    def __init__(
        self,
        piece_type: "PieceType",
        color: "PieceColor",
        board: "Board",
        x: int,
        y: int,
    ) -> None:
        self.piece_type = piece_type
        self.color = color
        self.board = board
        self.pos_x = x
        self.pos_y = y
        self.has_moved = False
        self.enpassant: tuple[int, int] | None = None
        self.is_invis = False
        board.tiles[y][x] = self

    def available_moves(self) -> list[tuple[int, int]]:
        possible_tiles: list[tuple[int, int]] = []
        is_checked = self.is_king_attacked()

        if self.piece_type == PieceType.KING:
            if not self.has_moved and not is_checked:  # castle
                for direction in king_castle_tiles():
                    for offset_x, offset_y in direction:
                        x = self.pos_x + offset_x
                        y = self.pos_y
                        if not self.board.is_in_bound(x, y):
                            break
                        same_row = self.board.get_piece(x, y)
                        if same_row is None:
                            continue
                        if (
                            self.is_any_piece(x, y)
                            and same_row.piece_type != PieceType.ROOK
                        ):
                            break
                        if offset_x in range(-2, 2) and self.is_coord_attacked(x, y):
                            break
                        if (
                            same_row.piece_type == PieceType.ROOK
                            and not same_row.has_moved
                        ):
                            possible_tiles.append((x, y))
            for offset_x in range(-1, 2):
                for offset_y in range(-1, 2):
                    if offset_x == 0 and offset_y == 0:
                        continue
                    x = self.pos_x + offset_x
                    y = self.pos_y + offset_y
                    if not self.board.is_in_bound(x, y):
                        continue
                    if self.is_ally(x, y):
                        continue
                    if self.is_coord_attacked(x, y):
                        continue
                    possible_tiles.append((x, y))
            if not is_checked:
                return possible_tiles
            new_possible_tile: list[tuple[int, int]] = []
            self.board.tiles[self.pos_y][self.pos_x] = None
            old_pos_x = self.pos_x
            old_pos_y = self.pos_y
            for possible_tile in possible_tiles:
                self.pos_x = possible_tile[0]
                self.pos_y = possible_tile[1]
                old_piece = self.board.get_piece(possible_tile[0], possible_tile[1])
                self.board.tiles[possible_tile[1]][possible_tile[0]] = self
                if not self.is_king_attacked():
                    new_possible_tile.append(possible_tile)
                self.board.tiles[possible_tile[1]][possible_tile[0]] = old_piece
            self.pos_x = old_pos_x
            self.pos_y = old_pos_y
            self.board.tiles[self.pos_y][self.pos_x] = self
            return new_possible_tile

        if not is_checked and self.is_pinned():
            return []
        match self.piece_type:
            case PieceType.ROOK:
                for direction in get_nsew():
                    self.__legit_moves(direction, possible_tiles)

            case PieceType.QUEEN:
                for direction in (*get_diagonals(), *get_nsew()):
                    self.__legit_moves(direction, possible_tiles)

            case PieceType.BISHOP:
                for direction in get_diagonals():
                    self.__legit_moves(direction, possible_tiles)

            case PieceType.KNIGHT:
                for offset_x, offset_y in KNIGHT_OFFSETS:
                    x = self.pos_x + offset_x
                    y = self.pos_y + offset_y
                    if not self.board.is_in_bound(x, y):
                        continue
                    if self.is_ally(x, y):
                        continue
                    possible_tiles.append((x, y))

            case PieceType.PAWN:
                if self.color == PieceColor.WHITE:
                    direction = 1
                elif self.color == PieceColor.BLACK:
                    direction = -1

                if self.enpassant is not None:
                    possible_tiles.append(self.enpassant)

                for x, y in (
                    (self.pos_x - 1, self.pos_y - direction),
                    (self.pos_x + 1, self.pos_y - direction),
                ):
                    if not self.board.is_in_bound(x, y):
                        continue
                    if self.is_enemy(x, y):
                        possible_tiles.append((x, y))

                for offset_y in range(1, 2 if self.has_moved else 3):
                    x = self.pos_x
                    y = self.pos_y - offset_y * direction
                    if not self.board.is_in_bound(x, y):
                        continue
                    if self.is_any_piece(x, y):
                        break
                    possible_tiles.append((x, y))

        if not is_checked:
            return possible_tiles
        new_possible_tile: list[tuple[int, int]] = []
        for possible_tile in possible_tiles:
            old_piece = self.board.get_piece(possible_tile[0], possible_tile[1])
            self.board.tiles[possible_tile[1]][possible_tile[0]] = self
            if not self.is_king_attacked():
                new_possible_tile.append(possible_tile)
            self.board.tiles[possible_tile[1]][possible_tile[0]] = old_piece
        return new_possible_tile

    def is_ally(self, x: int, y: int) -> bool:
        them = self.board.get_piece(x, y)
        if them is not None:
            return them.color == self.color
        return False

    def is_enemy(self, x: int, y: int) -> bool:
        them = self.board.get_piece(x, y)
        if them is not None:
            return them.color != self.color
        return False

    def is_any_piece(self, x: int, y: int) -> bool:
        return self.board.get_piece(x, y) is not None

    def __legit_moves(
        self,
        direction: Iterable[tuple[int, int]],
        possible_tiles: list[tuple[int, int]],
    ):
        for offset_x, offset_y in direction:
            x = self.pos_x + offset_x
            y = self.pos_y + offset_y
            if not self.board.is_in_bound(x, y):
                break
            if self.is_ally(x, y):
                break
            possible_tiles.append((x, y))
            if self.is_enemy(x, y):
                break

    def is_coord_attacked(self, x: int, y: int) -> bool:
        for direction in get_nsew():
            for offset_x, offset_y in direction:
                if not self.board.is_in_bound(x + offset_x, y + offset_y):
                    break
                selected_piece = self.board.get_piece(x + offset_x, y + offset_y)
                if selected_piece is None or selected_piece.is_invis:
                    continue
                if selected_piece.color == self.color:
                    break
                if selected_piece.piece_type in (PieceType.ROOK, PieceType.QUEEN):
                    return True
                break
        for direction in get_diagonals():
            for offset_x, offset_y in direction:
                if not self.board.is_in_bound(x + offset_x, y + offset_y):
                    break
                selected_piece = self.board.get_piece(x + offset_x, y + offset_y)
                if selected_piece is None or selected_piece.is_invis:
                    continue
                if selected_piece.color == self.color:
                    break
                if selected_piece.piece_type in (PieceType.BISHOP, PieceType.QUEEN):
                    return True
                break
        for offset_x, offset_y in KNIGHT_OFFSETS:
            if not self.board.is_in_bound(x + offset_x, y + offset_y):
                continue
            selected_piece = self.board.get_piece(x + offset_x, y + offset_y)
            if selected_piece is None:
                continue
            if (
                selected_piece.piece_type == PieceType.KNIGHT
                and selected_piece.color != self.color
            ):
                return True
        for offset_x in range(-1, 2):
            for offset_y in range(-1, 2):
                if offset_x == 0 and offset_y == 0:
                    continue
                if not self.board.is_in_bound(x + offset_x, y + offset_y):
                    continue
                selected_piece = self.board.get_piece(x + offset_x, y + offset_y)
                if selected_piece is None:
                    continue
                if (
                    selected_piece.piece_type == PieceType.KING
                    and selected_piece.color != self.color
                ):
                    return True
        if self.color == PieceColor.WHITE:
            pawn_direction = -1
        elif self.color == PieceColor.BLACK:
            pawn_direction = 1
        for offset_x, offset_y in (
            (-1, pawn_direction),
            (+1, pawn_direction),
        ):
            if not self.board.is_in_bound(x + offset_x, y + offset_y):
                continue
            selected_piece = self.board.get_piece(x + offset_x, y + offset_y)
            if selected_piece is None:
                continue
            if (
                selected_piece.piece_type == PieceType.PAWN
                and selected_piece.color != self.color
            ):
                return True
        return False

    def is_pinned(self) -> bool:
        self.is_invis = True
        is_king_attacked = self.is_king_attacked()
        self.is_invis = False
        return is_king_attacked

    def is_king_attacked(self) -> bool:
        if self.color == PieceColor.WHITE:
            king = self.board.white_king
        elif self.color == PieceColor.BLACK:
            king = self.board.black_king
        if king is None:
            raise Exception("How king dead")
        return self.is_coord_attacked(king.pos_x, king.pos_y)


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
