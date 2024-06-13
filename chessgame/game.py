import pygame
import sys
from . import background
from .board import Board, get_default_board
from .display import (
    render_pieces,
    get_image_dict,
    render_promotion,
    PIECE_TYPE_COUNT,
    PROMOTION_PIECE_TYPES,
)
from .piece import Piece, PieceColor


BACKGROUND_COLOR = (247, 202, 201)  # Rose Quartz
MIN_WIDTH = 640
MIN_HEIGHT = 480
FPS = 30
BLURRED_BLACK = (0, 0, 0, 192)


def run(screen: pygame.Surface):
    clock = pygame.time.Clock()
    board = get_default_board()
    images = get_image_dict()
    piece: Piece | None = None
    available_moves: list[tuple[int, int]] | None = None
    turn = PieceColor.WHITE
    while True:
        screen.fill(BACKGROUND_COLOR)
        pos_and_size = background.draw_checkers(screen, available_moves)
        render_pieces(screen, board.tiles, pos_and_size, images)
        if board.promoted_piece is not None:
            black_scrn = pygame.Surface(
                (screen.get_width(), screen.get_height()), pygame.SRCALPHA
            )
            black_scrn.fill(BLURRED_BLACK)
            screen.blit(black_scrn, (0, 0))
            offset_x, offset_y = render_promotion(
                screen, board.promoted_piece, pos_and_size, images
            )
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                return
            elif event.type == pygame.VIDEORESIZE:
                width, height = event.size  # type: ignore
                if width < MIN_WIDTH:
                    width = MIN_WIDTH
                if height < MIN_HEIGHT:
                    height = MIN_HEIGHT
                screen = pygame.display.set_mode((width, height), pygame.RESIZABLE)
            elif event.type == pygame.MOUSEBUTTONDOWN:
                if board.promoted_piece is not None:
                    pos_x, pos_y = pygame.mouse.get_pos()
                    index_x = (
                        pos_x - (pos_and_size[0] + pos_and_size[2] * offset_x)
                    ) // pos_and_size[2]
                    index_y = (
                        pos_y - (pos_and_size[1] + pos_and_size[3] * offset_y)
                    ) // pos_and_size[3]
                    if index_x not in range(PIECE_TYPE_COUNT) and index_y != 0:
                        continue
                    board.promoted_piece.piece_type = PROMOTION_PIECE_TYPES[
                        int(index_x)
                    ]
                    board.promoted_piece = None
                    continue

                coord = get_coord_on_click(board, pos_and_size)
                if coord is None:
                    continue
                if available_moves is not None and coord in available_moves:
                    assert piece is not None
                    board.move_piece(piece.pos_x, piece.pos_y, coord[0], coord[1])
                    available_moves = None
                    piece = None
                    if turn == PieceColor.WHITE:
                        turn = PieceColor.BLACK
                    elif turn == PieceColor.BLACK:
                        turn = PieceColor.WHITE
                    if is_game_over(board, turn):
                        get_winner(board, turn)
                        pygame.quit()
                    continue
                piece = board.get_piece(coord[0], coord[1])
                if piece is None or piece.color != turn:
                    piece = None
                    available_moves = None
                    continue
                available_moves = piece.available_moves()
        pygame.display.update()
        clock.tick(FPS)


def get_coord_on_click(
    board: Board, pos_and_size: tuple[int, int, int, int]
) -> tuple[int, int] | None:
    pos_x, pos_y = pygame.mouse.get_pos()
    index_x = (pos_x - pos_and_size[0]) // pos_and_size[2]
    index_y = (pos_y - pos_and_size[1]) // pos_and_size[3]
    if not board.is_in_bound(index_x, index_y):
        return None
    return index_x, index_y


def is_game_over(board: Board, turn: PieceColor) -> bool:
    can_move = False
    for piece in board.pieces_left:
        if piece.color != turn:
            continue
        if piece.available_moves:
            can_move = True
    return can_move


def get_winner(board: Board, turn: PieceColor) -> PieceColor | None:
    if turn == PieceColor.WHITE:
        if board.white_king is not None and board.white_king.is_king_attacked():
            print("Black Won")
        elif board.white_king is not None and not board.white_king.is_king_attacked():
            print("FOOL! you drawed the game.")
    elif turn == PieceColor.BLACK:
        if board.black_king is not None and board.black_king.is_king_attacked():
            print("White Won")
        elif board.black_king is not None and not board.black_king.is_king_attacked():
            print("FOOL! you drawed the game.")
