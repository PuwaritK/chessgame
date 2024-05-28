import pygame

# board goes from A to H columns and 1 to 8 rows (8*8)

LIGHT_BROWN = (232, 221, 176)
DARK_BROWN = (170, 141, 94)


def draw_checkers(screen: pygame.Surface):
    if screen.get_height() < screen.get_width():
        rect_height = screen.get_height() // 8
        rect_width = rect_height
        left = (screen.get_width() - screen.get_height()) // 2
        top = (screen.get_height() % rect_height) // 2
    else:
        rect_height = screen.get_width() // 8
        rect_width = rect_height
        left = (screen.get_width() % rect_width) // 2
        top = (screen.get_height() - screen.get_width()) // 2
    for i in range(8):
        for j in range(8):
            if i % 2 == 0:
                if j % 2 == 0:
                    pygame.draw.rect(
                        screen,
                        LIGHT_BROWN,
                        (
                            left + rect_width * j,
                            top + rect_height * i,
                            rect_width,
                            rect_height,
                        ),
                    )
                else:
                    pygame.draw.rect(
                        screen,
                        DARK_BROWN,
                        (
                            left + rect_width * j,
                            top + rect_height * i,
                            rect_width,
                            rect_height,
                        ),
                    )
            else:
                if j % 2 == 0:
                    pygame.draw.rect(
                        screen,
                        DARK_BROWN,
                        (
                            left + rect_width * j,
                            top + rect_height * i,
                            rect_width,
                            rect_height,
                        ),
                    )
                else:
                    pygame.draw.rect(
                        screen,
                        LIGHT_BROWN,
                        (
                            left + rect_width * j,
                            top + rect_height * i,
                            rect_width,
                            rect_height,
                        ),
                    )
