import pygame
from typing import Callable, Any


class Button:
    buttons: list["Button"] = []
    hover_buttons: list["Button"] = []
    hover_color = (170, 238, 187)
    unhover_color = (53, 53, 53)
    color = (0, 0, 0)

    def __init__(
        self,
        name: str,
        color: tuple[int, int, int],
        on_click: Callable[[], Any],
        left: int,
        top: int,
        width: int,
        height: int,
        hover: Callable[["Button"], Any] | None = None,
        unhover: Callable[["Button"], Any] = lambda _: None,
    ) -> None:
        self.button = pygame.Rect(left, top, width, height)
        self.name = name
        self.on_click = on_click
        self.color = color
        self.enable()
        if hover is not None:
            self.hover = hover
            self.unhover = unhover
            self.enable_hover()

    def enable(self):
        Button.buttons.append(self)

    def enable_hover(self):
        Button.hover_buttons.append(self)

    def disable(self):
        Button.buttons.remove(self)

    def is_mouse_on(self):
        return self.button.collidepoint(pygame.mouse.get_pos())
