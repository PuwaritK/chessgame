from typing import TYPE_CHECKING
import pygame

from abc import ABC, abstractmethod

from chessgame import background
from chessgame.board import Board, get_default_board
from chessgame.display import (
    PIECE_TYPE_COUNT,
    PROMOTION_PIECE_TYPES,
    get_image_dict,
    render_pieces,
    render_promotion,
)
from chessgame.piece import Piece, PieceColor

BACKGROUND_COLOR = (247, 202, 201)  # Rose Quartz
BLURRED_BLACK = (0, 0, 0, 192)
GAME_FONT = "Sans Serif"
BUTTON_TEXT_SIZE = 50
WINNER_SCENE_TEXT_SIZE = 150
MENU_FONT = 70


class Scene(ABC):
    @abstractmethod
    def on_click(self) -> "Scene | None":
        pass

    @abstractmethod
    def on_loop(self, screen: pygame.Surface):
        pass


class GameScene(Scene):
    def __init__(self) -> None:
        self.board = get_default_board()
        self.images = get_image_dict()
        self.piece: Piece | None = None
        self.available_moves: list[tuple[int, int]] | None = None
        self.turn = PieceColor.WHITE

    def on_click(self) -> "Scene | None":
        if self.board.promoted_piece is not None:
            pos_x, pos_y = pygame.mouse.get_pos()
            index_x = (
                pos_x
                - (
                    self.pos_and_size[0]
                    + self.pos_and_size[2] * self.promotion_offset_x
                )
            ) // self.pos_and_size[2]
            index_y = (
                pos_y
                - (
                    self.pos_and_size[1]
                    + self.pos_and_size[3] * self.promotion_offset_y
                )
            ) // self.pos_and_size[3]
            if index_x not in range(PIECE_TYPE_COUNT) and index_y != 0:
                return
            self.board.promoted_piece.piece_type = PROMOTION_PIECE_TYPES[int(index_x)]
            self.board.promoted_piece = None
            return

        coord = get_coord_on_click(self.board, self.pos_and_size)
        if coord is None:
            return
        if self.available_moves is not None and coord in self.available_moves:
            assert self.piece is not None
            self.board.move_piece(
                self.piece.pos_x, self.piece.pos_y, coord[0], coord[1]
            )
            self.available_moves = None
            self.piece = None
            if self.turn == PieceColor.WHITE:
                self.turn = PieceColor.BLACK
            elif self.turn == PieceColor.BLACK:
                self.turn = PieceColor.WHITE
            if not can_continue(self.board, self.turn):
                winner = get_winner(self.board, self.turn)
                return GameOverScene(winner)
            return
        self.piece = self.board.get_piece(coord[0], coord[1])
        if self.piece is None or self.piece.color != self.turn:
            self.piece = None
            self.available_moves = None
            return
        self.available_moves = self.piece.available_moves()

    def on_loop(self, screen: pygame.Surface):
        screen.fill(BACKGROUND_COLOR)
        self.pos_and_size = background.draw_checkers(screen, self.available_moves)
        render_pieces(screen, self.board.tiles, self.pos_and_size, self.images)
        if self.board.promoted_piece is not None:
            black_scrn = pygame.Surface(
                (screen.get_width(), screen.get_height()), pygame.SRCALPHA
            )
            black_scrn.fill(BLURRED_BLACK)
            screen.blit(black_scrn, (0, 0))
            self.promotion_offset_x, self.promotion_offset_y = render_promotion(
                screen, self.board.promoted_piece, self.pos_and_size, self.images
            )


class MenuScene(Scene):
    def __init__(self) -> None:
        self.menu_font = pygame.font.SysFont(GAME_FONT, MENU_FONT)
        self.button_font = pygame.font.SysFont(GAME_FONT, BUTTON_TEXT_SIZE)

    def on_click(self) -> "Scene | None":
        pos_x, pos_y = pygame.mouse.get_pos()
        if self.play_game_button_rect.collidepoint(pos_x, pos_y):
            return GameScene()
        elif self.settings_button_rect.collidepoint(pos_x, pos_y):
            return SettingScene()

    def on_loop(self, screen: pygame.Surface):
        screen.fill(BACKGROUND_COLOR)
        menu_title = self.menu_font.render("Goofy AHH Chessgame", True, (0, 0, 0))
        self.menu_text_rect = menu_title.get_rect(
            center=(screen.get_width() / 2, screen.get_height() / 8)
        )
        screen.blit(menu_title, self.menu_text_rect)

        play_game_button = self.button_font.render("Play", True, (0, 0, 0))
        self.play_game_button_rect = play_game_button.get_rect(
            center=(screen.get_width() / 2, screen.get_height() / 2)
        )
        screen.blit(play_game_button, self.play_game_button_rect)

        settings_button = self.button_font.render("Settings", True, (0, 0, 0))
        self.settings_button_rect = settings_button.get_rect(
            center=(
                screen.get_width() / 2,
                screen.get_height() / 2 + screen.get_height() / 8,
            )
        )
        screen.blit(settings_button, self.settings_button_rect)


class SettingScene(Scene):

    def on_click(self) -> "Scene | None":
        pass

    def on_loop(self, screen: pygame.Surface):
        pass


class GameOverScene(Scene):
    def __init__(self, winner: PieceColor | None) -> None:
        self.winner = winner
        self.winner_font = pygame.font.SysFont(GAME_FONT, WINNER_SCENE_TEXT_SIZE)
        self.button_font = pygame.font.SysFont(GAME_FONT, BUTTON_TEXT_SIZE)

    def on_click(self) -> "Scene | None":
        pos_x, pos_y = pygame.mouse.get_pos()
        if self.main_menu_button_rect.collidepoint(pos_x, pos_y):
            return MenuScene()

    def on_loop(self, screen: pygame.Surface):
        screen.fill(BACKGROUND_COLOR)
        main_menu_button = self.button_font.render("To Main Menu", True, (0, 0, 0))
        self.main_menu_button_rect = main_menu_button.get_rect(
            center=(
                screen.get_width() / 2,
                screen.get_height() / 2 + screen.get_height() / 4,
            )
        )
        screen.blit(main_menu_button, self.main_menu_button_rect)
        end_text = ""
        if self.winner == PieceColor.BLACK:
            end_text = "BLACK WON!"
        elif self.winner == PieceColor.WHITE:
            end_text = "WHITE WON!"
        else:
            end_text = "DRAW!"
        winner_title = self.winner_font.render(end_text, True, (0, 0, 0))
        winner_title_rect = winner_title.get_rect(
            center=(
                screen.get_width() / 2,
                screen.get_height() / 2,
            )
        )
        screen.blit(winner_title, winner_title_rect)


class Pause(Scene):
    pass


def get_coord_on_click(
    board: Board, pos_and_size: tuple[int, int, int, int]
) -> tuple[int, int] | None:
    pos_x, pos_y = pygame.mouse.get_pos()
    index_x = (pos_x - pos_and_size[0]) // pos_and_size[2]
    index_y = (pos_y - pos_and_size[1]) // pos_and_size[3]
    if not board.is_in_bound(index_x, index_y):
        return None
    return index_x, index_y


def can_continue(board: Board, turn: PieceColor) -> bool:
    for piece in board.pieces_left:
        if piece.color != turn:
            continue
        if piece.available_moves():
            return True
    return False


def get_winner(board: Board, turn: PieceColor) -> PieceColor | None:
    if turn == PieceColor.WHITE:
        king = board.white_king
        if king is not None and king.is_king_attacked():
            return PieceColor.BLACK
    elif turn == PieceColor.BLACK:
        king = board.black_king
        if king is not None and king.is_king_attacked():
            return PieceColor.WHITE
