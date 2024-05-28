import pygame

FPS = 30
WINDOW_WIDTH = 1280
WINDOW_HEIGHT = 720


def initialize() -> pygame.Surface:
    pygame.init()
    screen = pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT), pygame.RESIZABLE)
    clock = pygame.time.Clock()
    clock.tick(FPS)
    pygame.display.set_caption("Goofy AHH chessgame")
    return screen
