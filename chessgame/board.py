import pygame

# board goes from A to H columns and 1 to 8 rows (8*8)
LIGHT_BROWN = (232, 221, 176)
DARK_BROWN = (170, 141, 94)
LEFT = 280
TOP = 0


def draw_checkers(screen: pygame.Surface, rect_height=90, rect_width=90):
    for i in range(8):
        for j in range(8):
            if i % 2 == 0:
                if j % 2 == 0:
                    pygame.draw.rect(
                        screen,
                        LIGHT_BROWN,
                        (
                            LEFT + rect_width * j,
                            TOP + rect_height * j,
                            rect_width,
                            rect_height,
                        ),
                    )
                else:
                    pygame.draw.rect(
                        screen,
                        DARK_BROWN,
                        (
                            LEFT + rect_width * j,
                            TOP + rect_height * j,
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
                            LEFT + rect_width * j,
                            TOP + rect_height * j,
                            rect_width,
                            rect_height,
                        ),
                    )
                else:
                    pygame.draw.rect(
                        screen,
                        LIGHT_BROWN,
                        (
                            LEFT + rect_width * j,
                            TOP + rect_height * j,
                            rect_width,
                            rect_height,
                        ),
                    )
