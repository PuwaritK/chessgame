import pygame
from .piece import Piece, PieceType, PieceColor

WINDOW_WIDTH = 1280
WINDOW_HEIGHT = 720


def _get_image(file_name: str) -> pygame.Surface:
    return pygame.image.load(f"./chessgame/assets/{file_name}.png").convert_alpha()


IMAGES: dict[tuple[PieceColor, PieceType], pygame.Surface] = {
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
):
    for row in pieces:
        for piece in row:
            if piece is None:
                continue
            screen.blit(
                IMAGES[(piece.color, piece.piece_type)],
                (
                    pos_and_size[0] + piece.pos_x * pos_and_size[2],
                    pos_and_size[1] + piece.pos_y * pos_and_size[3],
                ),
                (
                    pos_and_size[2], pos_and_size[3]
                )
            )
