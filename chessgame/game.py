import pygame
import sys
from . import background
from .board import Board
from .display import (
    render_pieces,
    get_image_dict,
    render_promotion,
    PIECE_TYPE_COUNT,
    PROMOTION_PIECE_TYPES,
)
from .piece import Piece, PieceColor
from .scene import Scene, MenuScene, GameScene, Pause, Save, Load
from time import perf_counter

MIN_WIDTH = 640
MIN_HEIGHT = 480
FPS = 30


def run(screen: pygame.Surface):
    clock = pygame.time.Clock()
    scene = MenuScene()
    start_time = perf_counter()
    delta_time = 0
    pygame.key.set_repeat(200, 75)
    while True:
        event_check = scene.on_loop(screen, delta_time)
        if event_check is not None:
            scene = event_check
            continue

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
                event_check = scene.on_click(delta_time)
                if event_check is not None:
                    scene = event_check

            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    if type(scene) == GameScene:
                        scene = Pause(scene)
                    elif type(scene) == Pause:
                        scene = GameScene(scene)
                elif event.key == pygame.K_BACKSPACE:
                    if type(scene) == Save:
                        if scene.save_name_clicked:
                            scene.save_name = scene.save_name[0:-1]
                    elif type(scene) == Load:
                        if scene.load_name_clicked:
                            scene.load_name = scene.load_name[0:-1]
            elif event.type == pygame.TEXTINPUT:
                if type(scene) == Save:
                    scene.save_name += event.text
                if type(scene) == Load:
                    scene.load_name += event.text
        pygame.display.update()
        clock.tick(FPS)
        time_now = perf_counter()
        delta_time = time_now - start_time
        start_time = time_now
