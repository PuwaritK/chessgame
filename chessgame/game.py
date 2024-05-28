import pygame
from chessgame import board
import sys
from button import Button

BACKGROUND_COLOUR = (247, 202, 201)  # Rose Quartz


def run(screen: pygame.Surface):
    while True:
        screen.fill(BACKGROUND_COLOUR)
        board.draw_checkers(screen)
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
                pass

        for button in Button.buttons:
            if button.is_mouse_on():
                pass
            else:
                pass
        pygame.display.update()
