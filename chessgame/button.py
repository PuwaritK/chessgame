import pygame
from typing import Callable


class Button:
    buttons = []
    hover_buttons = []

    def __init__(
        self, name: str, func: Callable, left: int, top: int, width: int, height: int
    ) -> None:
        self.button = pygame.Rect(left, top, width, height)
        self.name = name
        self.func = func
        self.enable()

    def enable(self):
        Button.buttons.append(self)

    def disable(self):
        Button.buttons.remove(self)

    def is_mouse_on(self):
        return self.button.collidepoint(pygame.mouse.get_pos())
