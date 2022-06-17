from math import floor
import pygame
from random import randint
import sys

# Grid colours
LIGHT_GREY = (150, 150, 150)    # Lines
DARK_GREY = (50, 50, 50)        # BG

BLACK = (0, 0, 0)               # Pressed

WHITE = (255, 255, 255)         # For blank area

RED = (255, 0, 0)               # Flagged

# Number colours
LIGHT_BLUE = (150, 150, 255)    # 1, 2
BLUE = (0, 0, 255)              # 3, 4
YELLOW = (255, 255, 0)          # 5, 6
ORANGE = (255, 150, 0)          # 7, 8

BLOCKSIZE = 20

GRID_HEIGHT_PX = 500
WIDTH = 500
HEIGHT = 650
SCREEN_SIZE = (WIDTH, HEIGHT)

pygame.font.init()
COMICSANSMS = pygame.font.SysFont("comicsansms", 15)


pygame.init()
WIN = pygame.display.set_mode(SCREEN_SIZE)
pygame.display.set_caption("Alexis' Minesweeper")
clock = pygame.time.Clock()


def draw_grid() -> None:
    """
    Draws a grid on the screen with white space at the bottom 
    that can be used for buttons, score, time etc.

    Grid for loop, thanks to the answer in
    https://stackoverflow.com/questions/61061963/
    """
    WIN.fill(WHITE)
    grid_rect = pygame.Rect((0, 0), (500, 500))
    pygame.draw.rect(WIN, DARK_GREY, grid_rect)

    for x in range(WIDTH // BLOCKSIZE):
        for y in range(GRID_HEIGHT_PX // BLOCKSIZE):
            rect = pygame.Rect(x*BLOCKSIZE, y*BLOCKSIZE,
                               BLOCKSIZE, BLOCKSIZE)
            pygame.draw.rect(WIN, LIGHT_GREY, rect, 1)


def get_mines(number_of_mines) -> list:
    """
    Returns a list with coordinates of number_of_mines mines.
    """
    grid_width = WIDTH // BLOCKSIZE
    grid_height = GRID_HEIGHT_PX // BLOCKSIZE

    mine_rects = []
    for i in range(number_of_mines):
        rand_x = randint(0, grid_width) * 20
        rand_y = randint(0, grid_height) * 20
        minerect = pygame.Rect(rand_x, rand_y, BLOCKSIZE, BLOCKSIZE)
        mine_rects.append(minerect)

    return mine_rects


NUM_MINES = 100
MINES = get_mines(NUM_MINES)


def get_adjacent(pressrect: pygame.Rect):
    """
    Returns rects of adjacent spaces
    """
    x = pressrect.x
    y = pressrect.y
    
    rects = []

    # This is really messy.
    rects.append(pygame.Rect(x, y-BLOCKSIZE, BLOCKSIZE, BLOCKSIZE))
    # down
    rects.append(pygame.Rect(x, y+BLOCKSIZE, BLOCKSIZE, BLOCKSIZE))
    # left
    rects.append(pygame.Rect(x-BLOCKSIZE, y, BLOCKSIZE, BLOCKSIZE))
    # right
    rects.append(pygame.Rect(x+BLOCKSIZE, y, BLOCKSIZE, BLOCKSIZE))
    # upleft
    rects.append(pygame.Rect(x-BLOCKSIZE, y-BLOCKSIZE, BLOCKSIZE, BLOCKSIZE))
    # upright
    rects.append(pygame.Rect(x+BLOCKSIZE, y-BLOCKSIZE, BLOCKSIZE, BLOCKSIZE))
    # downright
    rects.append(pygame.Rect(x+BLOCKSIZE, y+BLOCKSIZE, BLOCKSIZE, BLOCKSIZE))
    # downleft
    rects.append(pygame.Rect(x-BLOCKSIZE, y+BLOCKSIZE, BLOCKSIZE, BLOCKSIZE))

    return rects


def count_mines(rect: pygame.Rect) -> int:
    """
    Count mines in adjacent spaces to rect 'rect'
    """
    adjacent_tiles = get_adjacent(rect)
    
    count = 0
    for tile in adjacent_tiles:
        if tile in MINES:
            count += 1

    return count


def get_mouse_rect(coords: tuple) -> pygame.Rect:
    """
    Returns a rect for the grid where the mouse is
    """
    mouse_x = coords[0]
    mouse_y = coords[1]
    floor_x = floor(mouse_x / BLOCKSIZE) * BLOCKSIZE
    floor_y = floor(mouse_y / BLOCKSIZE) * BLOCKSIZE
    mouse_grid_rect = pygame.Rect(
        floor_x, floor_y, BLOCKSIZE, BLOCKSIZE
        )

    return mouse_grid_rect


def main() -> None:
    """
    Main game method
    """
    pressed = []
    flagged = []

    while True:  
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

            elif event.type == pygame.MOUSEBUTTONDOWN:
                mouse_grid_rect = get_mouse_rect(pygame.mouse.get_pos())

                # What to do on a left click
                if event.button == 1:
                    if mouse_grid_rect in MINES:
                        mine_rect = mouse_grid_rect     # Abstraction
                        pygame.draw.rect(WIN, WHITE, mine_rect)
                        pygame.display.flip()
                        pygame.time.wait(1000)          # Wait 1s
                        pygame.quit()
                        sys.exit()
                    else:
                        click_rect = mouse_grid_rect    # Abstraction
                        pressed.append(click_rect)

                        # Press adjacent tiles
                        if len(pressed) > 0:
                            adjacent = get_adjacent(click_rect)
                            for square in adjacent:
                                pressed.append(square)
                
                # What do do on a right click
                elif event.button == 3:
                    if mouse_grid_rect not in flagged:  # if not flagged, flag
                        flagged.append(mouse_grid_rect)
                    else:                               # if flagged, unflag
                        flag_index = flagged.index(mouse_grid_rect)
                        del flagged[flag_index]

        draw_grid()

        revealed = []
        if len(pressed) > 0:
            for pressed_rect in pressed:
                pygame.draw.rect(WIN, BLACK, pressed_rect)
                
                adj = get_adjacent(pressed_rect)
                for tile in adj:
                    if tile not in MINES:
                        mines = count_mines(tile)
                        if mines != 0:
                            col = WHITE     # Default value to appease python
                            if mines <= 2:
                                col = LIGHT_BLUE
                            elif mines <= 4:
                                col = BLUE
                            elif mines <= 6:
                                col = YELLOW
                            else:
                                col = ORANGE

                            text = COMICSANSMS.render(f"{mines}", False, col)
                            revealed.append((text, tile))

        if len(revealed) > 0:
            for square in revealed:
                txt = square[0]
                rect = square[1]
                WIN.blit(txt, rect)

        if len(flagged) > 0:
            for flag in flagged:
                pygame.draw.rect(WIN, RED, flag)

        white_rect = pygame.Rect(
            0, GRID_HEIGHT_PX, 
            WIDTH, HEIGHT-GRID_HEIGHT_PX
            )
        pygame.draw.rect(WIN, WHITE, white_rect)

        pygame.display.update()
        clock.tick(12)


if __name__ == "__main__":
    main()