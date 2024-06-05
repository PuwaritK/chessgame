import pygame

from .piece import Piece, PieceType, PieceColor, TILES_COUNT_X, TILES_COUNT_Y
from time import sleep

WINDOW_WIDTH = 1280
WINDOW_HEIGHT = 720

PROMOTION_PIECE_TYPES = (
    PieceType.ROOK,
    PieceType.QUEEN,
    PieceType.BISHOP,
    PieceType.KNIGHT,
)

PIECE_TYPE_COUNT = len(PROMOTION_PIECE_TYPES)


def _get_image(file_name: str) -> pygame.Surface:
    return pygame.image.load(f"./chessgame/assets/{file_name}.png").convert_alpha()


IMAGES_PAIR_TYPE = dict[tuple[PieceColor, PieceType], pygame.Surface]


def get_image_dict() -> IMAGES_PAIR_TYPE:
    return {
        (PieceColor.WHITE, PieceType.KING): _get_image("white_king"),
        (PieceColor.WHITE, PieceType.KNIGHT): _get_image("white_knight"),
        (PieceColor.WHITE, PieceType.BISHOP): _get_image("white_bishop"),
        (PieceColor.WHITE, PieceType.PAWN): _get_image("white_pawn"),
        (PieceColor.WHITE, PieceType.QUEEN): _get_image("white_queen"),
        (PieceColor.WHITE, PieceType.ROOK): _get_image("white_rook"),
        (PieceColor.BLACK, PieceType.KING): _get_image("black_king"),
        (PieceColor.BLACK, PieceType.KNIGHT): _get_image("black_knight"),
        (PieceColor.BLACK, PieceType.BISHOP): _get_image("black_bishop"),
        (PieceColor.BLACK, PieceType.PAWN): _get_image("black_pawn"),
        (PieceColor.BLACK, PieceType.QUEEN): _get_image("black_queen"),
        (PieceColor.BLACK, PieceType.ROOK): _get_image("black_rook"),
    }


def initialize() -> pygame.Surface:
    pygame.init()
    screen = pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT), pygame.RESIZABLE)
    pygame.display.set_caption("Goofy AHH chessgame")
    return screen


def render_pieces(
    screen: pygame.Surface,
    pieces: list[list[Piece | None]],
    pos_and_size: tuple[int, int, int, int],
    images: IMAGES_PAIR_TYPE,
):
    for row in pieces:
        for piece in row:
            if piece is None:
                continue
            screen.blit(
                pygame.transform.scale(
                    images[(piece.color, piece.piece_type)],
                    (
                        pos_and_size[2],
                        pos_and_size[3],
                    ),
                ),
                (
                    pos_and_size[0] + piece.pos_x * pos_and_size[2],
                    pos_and_size[1] + piece.pos_y * pos_and_size[3],
                ),
            )


def render_promotion(
    screen: pygame.Surface,
    piece: Piece,
    pos_and_size: tuple[int, int, int, int],
    images: IMAGES_PAIR_TYPE,
) -> tuple[float, float]:
    left = pos_and_size[0]
    top = pos_and_size[1]
    rect_width = pos_and_size[2]
    rect_height = pos_and_size[3]
    offset_x = (TILES_COUNT_X - PIECE_TYPE_COUNT) / 2
    offset_y = (TILES_COUNT_Y - 1) / 2
    pygame.draw.rect(
        screen,
        (255, 0, 0),
        (
            left + rect_width * offset_x,
            top + rect_height * offset_y,
            PIECE_TYPE_COUNT * (rect_width),
            rect_height,
        ),
    )
    for i in range(4):
        screen.blit(
            pygame.transform.scale(
                images[(piece.color, PROMOTION_PIECE_TYPES[i])],
                (
                    rect_width,
                    rect_height,
                ),
            ),
            (
                left + rect_width * (offset_x + i),
                top + rect_height * offset_y,
            ),
        )
    return offset_x, offset_y
