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
from .scene import Scene, MenuScene, GameScene
from time import perf_counter

MIN_WIDTH = 640
MIN_HEIGHT = 480
FPS = 30


def run(screen: pygame.Surface):
    clock = pygame.time.Clock()
    scene = MenuScene()
    start_time = perf_counter()
    delta_time = 0
    while True:
        scene.on_loop(screen,delta_time)
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
        pygame.display.update()
        clock.tick(FPS)
        time_now = perf_counter()
        delta_time = time_now - start_time
        start_time = time_now
        
