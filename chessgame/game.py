import pygame
from chessgame import background
import sys
from .button import Button

BACKGROUND_COLOR = (247, 202, 201)  # Rose Quartz

FPS = 30


def run(screen: pygame.Surface):
    clock = pygame.time.Clock()
    while True:
        screen.fill(BACKGROUND_COLOR)
        background.draw_checkers(screen)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            elif event.type == pygame.VIDEORESIZE:
                width, height = event.size
                if width < 1280:
                    width = 1280
                if height < 720:
                    height = 720
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
