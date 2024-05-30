import pygame
import sys
from . import background
from .board import get_default_board
from .button import Button
from .display import render_pieces, get_image_dict

BACKGROUND_COLOR = (247, 202, 201)  # Rose Quartz
MIN_WIDTH = 640
MIN_HEIGHT = 480
FPS = 30


def run(screen: pygame.Surface):
    clock = pygame.time.Clock()
    board = get_default_board()
    images = get_image_dict()
    while True:
        screen.fill(BACKGROUND_COLOR)
        pos_and_size = background.draw_checkers(screen)
        render_pieces(screen, board.tiles, pos_and_size, images)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            elif event.type == pygame.VIDEORESIZE:
                width, height = event.size
                if width < MIN_WIDTH:
                    width = MIN_WIDTH
                if height < MIN_HEIGHT:
                    height = MIN_HEIGHT
                screen = pygame.display.set_mode((width, height), pygame.RESIZABLE)
            elif event.type == pygame.MOUSEBUTTONDOWN:
                for button in Button.buttons:
                    if button.is_mouse_on():
                        button.on_click()

        for button in Button.buttons:
            if button.is_mouse_on():
                button.hover(button)
            else:
                button.unhover(button)
            pygame.draw.rect(screen, (0, 0, 0), button.button)
        pygame.display.update()
        clock.tick(FPS)
