import pygame
from random import randint
import sys

# Grid colours
LIGHT_GREY = (150, 150, 150)    # Lines
DARK_GREY = (50, 50, 50)        # BG

BLACK = (0, 0, 0)               # Pressed

WHITE = (255, 255, 255)

RED = (255, 0, 0)               # Flagged

# Number colours
LIGHT_BLUE = (150, 150, 255)    # 1, 2
BLUE = (0, 0, 255)              # 3, 4
YELLOW = (255, 255, 0)          # 5, 6
ORANGE = (255, 150, 0)          # 7, 8

BLOCKSIZE = 20

GRID_HEIGHT = 500
WIDTH = 500
HEIGHT = 650
SCREEN_SIZE = (WIDTH, HEIGHT)

pygame.font.init()
COMICSANSMS = pygame.font.SysFont("comicsansms", 30)


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
        for y in range(GRID_HEIGHT // BLOCKSIZE):
            rect = pygame.Rect(x*BLOCKSIZE, y*BLOCKSIZE,
                               BLOCKSIZE, BLOCKSIZE)
            pygame.draw.rect(WIN, LIGHT_GREY, rect, 1)


def main() -> None:
    """
    Main game method
    """
    while True:  
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

        draw_grid()
        pygame.display.update()
        clock.tick(12)



if __name__ == "__main__":
    main()