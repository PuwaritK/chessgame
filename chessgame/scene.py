from typing import TYPE_CHECKING
import pygame
import json
from abc import ABC, abstractmethod
import os
from pathlib import Path
from chessgame import background, piece
from chessgame.board import Board, get_default_board
from chessgame.display import (
    PIECE_TYPE_COUNT,
    PROMOTION_PIECE_TYPES,
    get_image_dict,
    render_pieces,
    render_promotion,
)
from chessgame.piece import Piece, PieceColor, PieceType

BACKGROUND_COLOR = (247, 202, 201)  # Rose Quartz
BLURRED_BLACK = (0, 0, 0, 192)
GAME_FONT = "Sans Serif"
BUTTON_TEXT_SIZE = 50
WINNER_SCENE_TEXT_SIZE = 150
MENU_FONT = 70
TEXT_FONT = 22
TIME_CONTROL = [15, 10]  # 15 minutes | 10 seconds increment


class Scene(ABC):
    @abstractmethod
    def on_click(self, delta_time: float) -> "Scene | None":
        pass

    @abstractmethod
    def on_loop(self, screen: pygame.Surface, delta_time: float):
        pass


class GameScene(Scene):
    def __init__(self, scene: Scene | None = None) -> None:
        if scene is None:
            self.time_control = TIME_CONTROL
            self.save_name = ""
            self.board = get_default_board()
            self.images = get_image_dict()
            self.piece: Piece | None = None
            self.available_moves: list[tuple[int, int]] | None = None
            self.turn = PieceColor.WHITE
            self.text_font = pygame.font.SysFont(GAME_FONT, TEXT_FONT)
            self.white_time = 60 * self.time_control[0]
            self.black_time = 60 * self.time_control[0]
            self.game_time = 0

        elif isinstance(scene, Pause):
            self.time_control = scene.time_control
            self.save_name = scene.save_name
            self.board = scene.board
            self.images = scene.images
            self.piece: Piece | None = scene.piece
            self.available_moves: list[tuple[int, int]] | None = scene.available_moves
            self.turn = scene.turn
            self.text_font = pygame.font.SysFont(GAME_FONT, TEXT_FONT)
            self.white_time = scene.white_time
            self.black_time = scene.black_time
            self.game_time = scene.game_time

        elif isinstance(scene, Load):
            self.time_control = scene.time_control
            self.save_name = scene.load_name
            self.board = scene.board
            self.images = get_image_dict()
            self.piece: Piece | None = scene.piece
            if self.piece is None:
                self.available_moves = None
            else:
                self.available_moves: list[tuple[int, int]] | None = (
                    self.piece.available_moves()
                )
            self.turn = scene.turn
            self.text_font = pygame.font.SysFont(GAME_FONT, TEXT_FONT)
            self.white_time = scene.white_time
            self.black_time = scene.black_time
            self.game_time = scene.game_time

    def on_click(self, delta_time: float) -> "Scene | None":
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
            assert self.white_time is not None
            assert self.black_time is not None
            assert self.turn is not None
            if self.turn == PieceColor.WHITE:
                self.white_time += TIME_CONTROL[1]
                self.turn = PieceColor.BLACK
            elif self.turn == PieceColor.BLACK:
                self.black_time += TIME_CONTROL[1]
                self.turn = PieceColor.WHITE
            if not can_continue(self.board, self.turn):
                winner = get_winner(self.board, self.turn)
                return GameOverScene(winner, self.save_name)
            return
        self.piece = self.board.get_piece(coord[0], coord[1])
        if self.piece is None or self.piece.color != self.turn:
            self.piece = None
            self.available_moves = None
            return
        self.available_moves = self.piece.available_moves()

    def on_loop(self, screen: pygame.Surface, delta_time: float):
        screen.fill(BACKGROUND_COLOR)
        assert self.white_time is not None
        assert self.black_time is not None
        assert self.game_time is not None
        if self.white_time < 0:
            return GameOverScene(PieceColor.BLACK, self.save_name)
        if self.black_time < 0:
            return GameOverScene(PieceColor.WHITE, self.save_name)

        game_time = self.text_font.render(
            f"Game Time: {self.game_time//60} minutes {self.game_time:.2f} seconds",
            True,
            (0, 0, 0),
        )
        self.game_time_rect = game_time.get_rect(
            center=(screen.get_width() * 4 / 32, screen.get_height() * 1 / 16)
        )

        white_time = self.text_font.render(
            f"White Time: {self.white_time:.2f} seconds",
            True,
            (0, 0, 0),
        )
        self.white_time_rect = white_time.get_rect(
            center=(screen.get_width() * 3 / 32, screen.get_height() * 2 / 16)
        )

        black_time = self.text_font.render(
            f"Black Time: {self.black_time:.2f} seconds",
            True,
            (0, 0, 0),
        )
        self.black_time_rect = black_time.get_rect(
            center=(screen.get_width() * 3 / 32, screen.get_height() * 3 / 16)
        )

        screen.blit(game_time, self.game_time_rect)
        screen.blit(white_time, self.white_time_rect)
        screen.blit(black_time, self.black_time_rect)

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
        if self.turn == PieceColor.WHITE:
            self.white_time -= delta_time
        elif self.turn == PieceColor.BLACK:
            self.black_time -= delta_time
        self.game_time += delta_time


class MenuScene(Scene):
    def __init__(self) -> None:
        self.menu_font = pygame.font.SysFont(GAME_FONT, MENU_FONT)
        self.button_font = pygame.font.SysFont(GAME_FONT, BUTTON_TEXT_SIZE)

    def on_click(self, delta_time: float) -> "Scene | None":
        pos_x, pos_y = pygame.mouse.get_pos()
        if self.play_game_button_rect.collidepoint(pos_x, pos_y):
            return GameScene()
        elif self.settings_button_rect.collidepoint(pos_x, pos_y):
            return SettingScene()
        elif self.load_game_button_rect.collidepoint(pos_x, pos_y):
            return Load()

    def on_loop(self, screen: pygame.Surface, delta_time: float):
        screen.fill(BACKGROUND_COLOR)
        menu_title = self.menu_font.render("Simple Chessgame", True, (0, 0, 0))

        self.menu_text_rect = menu_title.get_rect(
            center=(screen.get_width() / 2, screen.get_height() / 8)
        )
        screen.blit(menu_title, self.menu_text_rect)

        play_game_button = self.button_font.render("New Game", True, (0, 0, 0))
        self.play_game_button_rect = play_game_button.get_rect(
            center=(screen.get_width() / 2, screen.get_height() / 2)
        )
        screen.blit(play_game_button, self.play_game_button_rect)

        load_game_button = self.button_font.render("Load Game", True, (0, 0, 0))
        self.load_game_button_rect = load_game_button.get_rect(
            center=(
                screen.get_width() / 2,
                screen.get_height() / 2 + screen.get_height() / 8,
            )
        )
        screen.blit(load_game_button, self.load_game_button_rect)

        settings_button = self.button_font.render("Settings", True, (0, 0, 0))
        self.settings_button_rect = settings_button.get_rect(
            center=(
                screen.get_width() / 2,
                screen.get_height() / 2 + screen.get_height() / 4,
            )
        )
        screen.blit(settings_button, self.settings_button_rect)


class SettingScene(Scene):
    def __init__(self) -> None:
        self.menu_font = pygame.font.SysFont(GAME_FONT, MENU_FONT)
        self.button_font = pygame.font.SysFont(GAME_FONT, BUTTON_TEXT_SIZE)
        self.configuring_time_control = False

    def on_click(self, delta_time: float) -> "Scene | None":
        pos_x, pos_y = pygame.mouse.get_pos()

        if self.time_control_button_rect.collidepoint(pos_x, pos_y):
            self.configuring_time_control = True
            return
        if self.return_button_rect.collidepoint(pos_x, pos_y):
            return MenuScene()

        if self.configuring_time_control:
            if self.confirm_button_rect.collidepoint(pos_x, pos_y):
                self.configuring_time_control = False

            if self.minute_up_button_rect.collidepoint(pos_x, pos_y):
                TIME_CONTROL[0] += 1
            if self.minute_down_button_rect.collidepoint(pos_x, pos_y):
                if TIME_CONTROL[0] > 1:
                    TIME_CONTROL[0] -= 1

            if self.second_up_button_rect.collidepoint(pos_x, pos_y):
                TIME_CONTROL[1] += 1
            if self.second_down_button_rect.collidepoint(pos_x, pos_y):
                if TIME_CONTROL[1] > 0:
                    TIME_CONTROL[1] -= 1

    def on_loop(self, screen: pygame.Surface, delta_time: float):
        screen.fill(BACKGROUND_COLOR)
        if not self.configuring_time_control:
            time_control_button = self.button_font.render(
                "Configure Time Control", True, (0, 0, 0)
            )
            self.time_control_button_rect = time_control_button.get_rect(
                center=(screen.get_width() / 2, screen.get_height() / 2)
            )
            return_button = self.button_font.render("Return", True, (0, 0, 0))
            self.return_button_rect = return_button.get_rect(
                center=(screen.get_width() / 2, screen.get_height() * 3 / 4)
            )
            screen.blit(time_control_button, self.time_control_button_rect)
            screen.blit(return_button, self.return_button_rect)
        else:
            time_control_text = self.menu_font.render(
                f"{TIME_CONTROL[0]} | {TIME_CONTROL[1]}", True, (0, 0, 0)
            )
            time_control_text_rect = time_control_text.get_rect(
                center=(screen.get_width() / 2, screen.get_height() / 2)
            )
            screen.blit(time_control_text, time_control_text_rect)

            minute_up_button = self.button_font.render(
                "Increase Minutes", True, (0, 0, 0)
            )
            self.minute_up_button_rect = minute_up_button.get_rect(
                center=(screen.get_width() * 1 / 8, screen.get_height() * 3 / 4)
            )
            minute_down_button = self.button_font.render(
                "Decrease Minutes", True, (0, 0, 0)
            )
            self.minute_down_button_rect = minute_down_button.get_rect(
                center=(screen.get_width() * 3 / 8, screen.get_height() * 3 / 4)
            )

            second_up_button = self.button_font.render(
                "Increase Seconds", True, (0, 0, 0)
            )
            self.second_up_button_rect = second_up_button.get_rect(
                center=(screen.get_width() * 5 / 8, screen.get_height() * 3 / 4)
            )
            second_down_button = self.button_font.render(
                "Decrease Seconds", True, (0, 0, 0)
            )
            self.second_down_button_rect = second_down_button.get_rect(
                center=(screen.get_width() * 7 / 8, screen.get_height() * 3 / 4)
            )

            confirm_button = self.button_font.render("Confirm Change", True, (0, 0, 0))
            self.confirm_button_rect = confirm_button.get_rect(
                center=(screen.get_width() * 1 / 2, screen.get_height() * 7 / 8)
            )

            screen.blit(minute_up_button, self.minute_up_button_rect)
            screen.blit(minute_down_button, self.minute_down_button_rect)
            screen.blit(second_up_button, self.second_up_button_rect)
            screen.blit(second_down_button, self.second_down_button_rect)
            screen.blit(confirm_button, self.confirm_button_rect)


class GameOverScene(Scene):
    def __init__(self, winner: PieceColor | None, save_name: str) -> None:
        self.winner = winner
        self.winner_font = pygame.font.SysFont(GAME_FONT, WINNER_SCENE_TEXT_SIZE)
        self.button_font = pygame.font.SysFont(GAME_FONT, BUTTON_TEXT_SIZE)
        self.save_name = save_name

    def on_click(self, delta_time: float) -> "Scene | None":
        pos_x, pos_y = pygame.mouse.get_pos()
        if self.main_menu_button_rect.collidepoint(pos_x, pos_y):
            return MenuScene()

    def on_loop(self, screen: pygame.Surface, delta_time: float):
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

        try:
            os.remove(Path(f"saves/{self.save_name}.json"))

        except OSError:
            pass
        winner_title = self.winner_font.render(end_text, True, (0, 0, 0))
        winner_title_rect = winner_title.get_rect(
            center=(
                screen.get_width() / 2,
                screen.get_height() / 2,
            )
        )
        screen.blit(winner_title, winner_title_rect)


class Pause(Scene):
    def __init__(self, scene: GameScene) -> None:
        self.time_control = scene.time_control
        self.save_name = scene.save_name
        self.menu_font = pygame.font.SysFont(GAME_FONT, MENU_FONT)
        self.button_font = pygame.font.SysFont(GAME_FONT, BUTTON_TEXT_SIZE)
        self.board = scene.board
        self.images = scene.images
        self.piece: Piece | None = scene.piece
        self.available_moves: list[tuple[int, int]] | None = scene.available_moves
        self.turn = scene.turn
        self.text_font = pygame.font.SysFont(GAME_FONT, TEXT_FONT)
        self.white_time = scene.white_time
        self.black_time = scene.black_time
        self.game_time = scene.game_time

    def on_click(self, delta_time: float) -> Scene | None:
        pos_x, pos_y = pygame.mouse.get_pos()

        if self.return_button_rect.collidepoint(pos_x, pos_y):
            return GameScene(self)
        if self.save_button_rect.collidepoint(pos_x, pos_y):
            return Save(self)

    def on_loop(self, screen: pygame.Surface, delta_time: float):
        screen.fill(BACKGROUND_COLOR)
        title = self.menu_font.render("Game Paused", True, (0, 0, 0))
        title_rect = title.get_rect(
            center=(screen.get_width() / 2, screen.get_height() / 4)
        )
        screen.blit(title, title_rect)

        return_button = self.button_font.render("Return To Game", True, (0, 0, 0))
        self.return_button_rect = return_button.get_rect(
            center=(screen.get_width() / 2, screen.get_height() / 2)
        )
        screen.blit(return_button, self.return_button_rect)

        save_button = self.button_font.render("Save Game", True, (0, 0, 0))
        self.save_button_rect = save_button.get_rect(
            center=(screen.get_width() / 2, screen.get_height() * 3 / 4)
        )
        screen.blit(save_button, self.save_button_rect)


class Save(Scene):
    def __init__(self, scene: Pause) -> None:
        self.menu_font = pygame.font.SysFont(GAME_FONT, MENU_FONT)
        self.button_font = pygame.font.SysFont(GAME_FONT, BUTTON_TEXT_SIZE)
        self.save_name = ""
        self.board = scene.board
        self.images = scene.images
        self.piece: Piece | None = scene.piece
        self.available_moves: list[tuple[int, int]] | None = scene.available_moves
        self.turn = scene.turn
        self.text_font = pygame.font.SysFont(GAME_FONT, TEXT_FONT)
        self.white_time = scene.white_time
        self.black_time = scene.black_time
        self.game_time = scene.game_time
        self.save_name_clicked = False

    def on_click(self, delta_time: float) -> Scene | None:
        pos_x, pos_y = pygame.mouse.get_pos()

        if (
            self.save_name_button_rect.collidepoint(pos_x, pos_y)
            and not self.save_name_clicked
        ):
            self.save_name_clicked = True
            pygame.key.start_text_input()
        elif (
            self.save_name_button_rect.collidepoint(pos_x, pos_y)
            and self.save_name_clicked
        ) or (
            not self.save_name_button_rect.collidepoint(pos_x, pos_y)
            and self.save_name_clicked
        ):
            self.save_name_clicked = False
            pygame.key.stop_text_input()
        elif self.save_button_rect.collidepoint(pos_x, pos_y):
            self.save_name_clicked = False
            pygame.key.stop_text_input()
            with open(f".\\saves\\{self.save_name}.json", "w") as f:
                data_to_save = {}
                piece_on_board = []
                for row in self.board.tiles:
                    for tiles in row:
                        if tiles is None:
                            piece_on_board.append(None)
                        else:
                            appending_piece_attributes = [
                                tiles.color.value,
                                tiles.piece_type.value,
                                tiles.enpassant,
                                tiles.has_moved,
                                tiles.is_invis,
                                tiles.pos_x,
                                tiles.pos_y,
                            ]
                            piece_on_board.append(appending_piece_attributes)
                data_to_save["piece_on_board"] = piece_on_board
                data_to_save["TIME_CONTROL"] = TIME_CONTROL
                data_to_save["game_time"] = self.game_time
                data_to_save["white_time"] = self.white_time
                data_to_save["black_time"] = self.black_time
                data_to_save["turn"] = self.turn.value
                # if self.piece is not None:
                #     f.write(f"[{self.piece.pos_x}, {self.piece.pos_y}]\n")
                # else:
                #     f.write(f"{None}")
                json.dump(data_to_save, f)

    def on_loop(self, screen: pygame.Surface, delta_time: float):
        screen.fill(BACKGROUND_COLOR)
        save_name_button = self.button_font.render(
            f"Save Name: {self.save_name}", True, (0, 0, 0)
        )
        self.save_name_button_rect = save_name_button.get_rect(
            center=(screen.get_width() / 2, screen.get_height() / 2)
        )
        screen.blit(save_name_button, self.save_name_button_rect)

        save_button = self.button_font.render("Save", True, (0, 0, 0))
        self.save_button_rect = save_button.get_rect(
            center=(screen.get_width() / 2, screen.get_height() * 3 / 4)
        )
        screen.blit(save_button, self.save_button_rect)


class Load(Scene):
    def __init__(self) -> None:
        self.menu_font = pygame.font.SysFont(GAME_FONT, MENU_FONT)
        self.button_font = pygame.font.SysFont(GAME_FONT, BUTTON_TEXT_SIZE)
        self.text_font = pygame.font.SysFont(GAME_FONT, TEXT_FONT)
        self.load_name = ""
        self.load_name_clicked = False
        self.load_error = False
        self.board: Board
        self.piece: Piece | None = None
        self.turn: PieceColor
        self.white_time: float | None = None
        self.black_time: float | None = None
        self.game_time: float | None = None
        self.time_control: list[int]

    def on_click(self, delta_time: float) -> Scene | None:
        pos_x, pos_y = pygame.mouse.get_pos()

        if self.return_botton_rect.collidepoint(pos_x, pos_y):
            return MenuScene()
        elif (
            self.load_name_button_rect.collidepoint(pos_x, pos_y)
            and not self.load_name_clicked
        ):
            self.load_name_clicked = True
            pygame.key.start_text_input()
        elif (
            self.load_name_button_rect.collidepoint(pos_x, pos_y)
            and self.load_name_clicked
        ) or (
            not self.load_name_button_rect.collidepoint(pos_x, pos_y)
            and self.load_name_clicked
        ):
            self.load_name_clicked = False
            pygame.key.stop_text_input()
        elif self.load_button_rect.collidepoint(pos_x, pos_y):
            self.load_name_clicked = False
            self.load_error = False
            pygame.key.stop_text_input()
            try:
                with open(f".\\saves\\{self.load_name}.json", "r") as f:
                    game_data = json.load(f)
                    piece_on_board = game_data["piece_on_board"]
                    self.board = Board()
                    for piece in piece_on_board:
                        if piece is None:
                            self.board.tiles.append([None])
                            continue
                        created_piece = Piece(
                            PieceType(piece[1]),
                            PieceColor(piece[0]),
                            self.board,
                            piece[5],
                            piece[6],
                        )
                        created_piece.enpassant = piece[2]
                        created_piece.has_moved = piece[3]
                        created_piece.is_invis = piece[4]
                        self.board.pieces_left.append(created_piece)
                    self.time_control = game_data["TIME_CONTROL"]
                    self.game_time = game_data["game_time"]
                    self.white_time = game_data["white_time"]
                    self.black_time = game_data["black_time"]
                    self.turn = PieceColor(game_data["turn"])
                    # self.save_name = ...
                return GameScene(self)
            except OSError:
                self.load_error = True

    def on_loop(self, screen: pygame.Surface, delta_time: float):
        screen.fill(BACKGROUND_COLOR)

        load_name_button = self.button_font.render(
            f"Load Save Name: {self.load_name}", True, (0, 0, 0)
        )
        self.load_name_button_rect = load_name_button.get_rect(
            center=(screen.get_width() / 2, screen.get_height() / 2)
        )
        screen.blit(load_name_button, self.load_name_button_rect)

        load_button = self.button_font.render("Load", True, (0, 0, 0))
        self.load_button_rect = load_button.get_rect(
            center=(screen.get_width() / 2, screen.get_height() * 3 / 4)
        )
        screen.blit(load_button, self.load_button_rect)

        return_button = self.button_font.render("Return", True, (0, 0, 0))
        self.return_botton_rect = return_button.get_rect(
            center=(screen.get_width() / 2, screen.get_height() * 7 / 8)
        )
        screen.blit(return_button, self.return_botton_rect)

        if self.load_error:
            error_text = self.menu_font.render(
                "Game name does not exists!", True, (0, 0, 0)
            )
            error_text_rect = error_text.get_rect(
                center=(
                    screen.get_width() / 2,
                    screen.get_height() - self.menu_font.get_height() * 2,
                )
            )
            screen.blit(error_text, error_text_rect)


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
