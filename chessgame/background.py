import pygame

# board goes from A to H columns and 1 to 8 rows (8*8)

LIGHT_BROWN = pygame.Color(232, 221, 176)
DARK_BROWN = pygame.Color(170, 141, 94)
GREEN = pygame.Color(15, 157, 88)


def draw_checkers(
    screen: pygame.Surface, available_moves: list[tuple[int, int]] | None
) -> tuple[int, int, int, int]:
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
            if available_moves is not None and (j, i) in available_moves:
                light_brown = LIGHT_BROWN.lerp(GREEN, 0.3)
                dark_brown = DARK_BROWN.lerp(GREEN, 0.3)
            else:
                light_brown = LIGHT_BROWN
                dark_brown = DARK_BROWN
            if i % 2 == 0:
                if j % 2 == 0:
                    pygame.draw.rect(
                        screen,
                        light_brown,
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
                        dark_brown,
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
                        dark_brown,
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
                        light_brown,
                        (
                            left + rect_width * j,
                            top + rect_height * i,
                            rect_width,
                            rect_height,
                        ),
                    )
    return left, top, rect_width, rect_height
