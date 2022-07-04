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

# Measurements
BLOCKSIZE = 20
GRID_HEIGHT_PX = 500
WIDTH = 500
HEIGHT = 650
SCREEN_SIZE = (WIDTH, HEIGHT)

# Pygame inits
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
    """
    WIN.fill(WHITE) # Despite a white rect being drawn later this is needed
    grid_rect = pygame.Rect((0, 0), (500, 500))
    pygame.draw.rect(WIN, DARK_GREY, grid_rect)

    # Grid for loop, thanks to the answer in
    # https://stackoverflow.com/questions/61061963/
    for x in range(WIDTH // BLOCKSIZE):
        for y in range(GRID_HEIGHT_PX // BLOCKSIZE):
            rect = pygame.Rect(x*BLOCKSIZE, y*BLOCKSIZE,
                               BLOCKSIZE, BLOCKSIZE)
            pygame.draw.rect(WIN, LIGHT_GREY, rect, 1)


def get_mines(number_of_mines) -> list:
    """
    Returns a list with coordinates of number_of_mines mines.
    """
    # Get the dimensions in terms of tiles
    grid_width = WIDTH // BLOCKSIZE
    grid_height = GRID_HEIGHT_PX // BLOCKSIZE

    mine_rects = []
    
    # For each mine
    for i in range(number_of_mines):
        generated = False                           # Marker for valid      
        while not generated:                        # Wait for a valid
            rand_x = randint(0, grid_width-1) * 20  # Get x for rect
            rand_y = randint(0, grid_height-1) * 20 # Get y for rect
            minerect = pygame.Rect(rand_x, rand_y, BLOCKSIZE, BLOCKSIZE)
            
            # Check if the generated rect is already a mine
            if minerect not in mine_rects:
                generated = True                    # Mark valid
        
        mine_rects.append(minerect)                 # Add to rects

    mine_rects = mine_rects[:100]   # Assure only 100 mine rects

    return mine_rects


NUM_MINES = 100
MINES = get_mines(NUM_MINES)


def get_adjacent(pressrect: pygame.Rect):
    """
    Returns rects of adjacent spaces
    """
    # Get x, y of pressed rect
    x = pressrect.x
    y = pressrect.y
    
    rects = []

    """
    This is really messy.
    This changes the x and y values and makes rects from them
    These are the rects for up, down, left, right, up-left, up-right
    down-right, and down-left from the pressed rect.
    """
    # up
    rects.append(pygame.Rect(x, y-BLOCKSIZE, BLOCKSIZE, BLOCKSIZE))
    # down
    rects.append(pygame.Rect(x, y+BLOCKSIZE, BLOCKSIZE, BLOCKSIZE))
    # left
    rects.append(pygame.Rect(x-BLOCKSIZE, y, BLOCKSIZE, BLOCKSIZE))
    # right
    rects.append(pygame.Rect(x+BLOCKSIZE, y, BLOCKSIZE, BLOCKSIZE))
    # up-left
    rects.append(pygame.Rect(x-BLOCKSIZE, y-BLOCKSIZE, BLOCKSIZE, BLOCKSIZE))
    # up-right
    rects.append(pygame.Rect(x+BLOCKSIZE, y-BLOCKSIZE, BLOCKSIZE, BLOCKSIZE))
    # down-right
    rects.append(pygame.Rect(x+BLOCKSIZE, y+BLOCKSIZE, BLOCKSIZE, BLOCKSIZE))
    # down-left
    rects.append(pygame.Rect(x-BLOCKSIZE, y+BLOCKSIZE, BLOCKSIZE, BLOCKSIZE))

    return rects


def count_mines(rect: pygame.Rect) -> int:
    """
    Count mines in adjacent spaces to rect 'rect'
    """
    # Get rects of adjacent tile to rect 
    adjacent_tiles = get_adjacent(rect)
    
    # Iterate through adjacent rects and increment count 
    # for each match to a rect in MINES.
    count = 0
    for tile in adjacent_tiles:
        if tile in MINES:
            count += 1

    return count


def get_mouse_rect(coords: tuple) -> pygame.Rect:
    """
    Returns a rect for the grid where the mouse is

    Used by putting the value from a get_pos in as coords
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
    # Initialise some variables outside loop so they do not reset each frame
    pressed = []
    flagged = []
    numbered = []
    ticks_passed = 0

    def draw_flags():
        """
        Draw the flags
        """
        if len(flagged) > 0:                # Fill in flagged spaces
            for flag in flagged:
                pygame.draw.rect(WIN, RED, flag)

    # Main game loop
    while True:  
        draw_grid()

        if len(pressed) > 0:                # Fill in pressed spaces
            for pressed_rect in pressed:
                pygame.draw.rect(WIN, BLACK, pressed_rect)

        revealed = []                       # Do the numbers
        if len(pressed) > 0:        
            for pressed_rect in pressed:
                adj = get_adjacent(pressed_rect)    # Get adjacent tiles
                for tile in adj:                    # For each adjacent
                    if tile not in MINES:           # If its not a mine
                        mines = count_mines(tile)   # Count adjacent mines

                        # If the tile has adjacent mines, assign a value that
                        # represents the colour of the text on the tile.
                        if mines != 0:
                            col = WHITE     # Default value
                            if mines <= 2:
                                col = LIGHT_BLUE
                            elif mines <= 4:
                                col = BLUE
                            elif mines <= 6:
                                col = YELLOW
                            else:
                                col = ORANGE

                            # Draw a dark grey tile if it is numbered 
                            pygame.draw.rect(WIN, DARK_GREY, tile)

                            # Add the text and tile to lists to be used later
                            text = COMICSANSMS.render(f" {mines}", False, col)
                            revealed.append((text, tile))
                            numbered.append(tile)

        # Event checker
        for event in pygame.event.get():
            # Check for quit
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

            # If not quit check for mouse down
            elif event.type == pygame.MOUSEBUTTONDOWN:
                # Get grid rect corresponding to where mouse clicked
                mouse_grid_rect = get_mouse_rect(pygame.mouse.get_pos())

                # What to do on a left click
                if event.button == 1:
                    if mouse_grid_rect in MINES:        # If clicked is a mine   
                        draw_flags()                    # Draw all flags 
                        for mine in MINES:              # Draw all mines                
                            pygame.draw.rect(WIN, WHITE, mine)

                        pygame.display.flip()

                        # Wait 2s then quit game
                        pygame.time.wait(2000)
                        pygame.quit()                   
                        sys.exit()

                    else:
                        click_rect = mouse_grid_rect    # Abstraction

                        # Stop user from clicking on numbered tiles
                        # as this is a 'cheese' strategy.
                        if click_rect not in numbered:
                            pressed.append(click_rect)

                            # Press adjacent tiles
                            if len(pressed) > 0:
                                adjacent = get_adjacent(click_rect)
                                for square in adjacent:
                                    pressed.append(square)
                
                # What do do on a right click
                elif event.button == 3:
                    # Check if mouse is in bounds of the grid
                    in_bounds = False
                    if mouse_grid_rect.x < WIDTH:
                        if mouse_grid_rect.y < GRID_HEIGHT_PX:
                            in_bounds = True

                    # If mouse is in bounds...
                    if in_bounds:   
                        if mouse_grid_rect not in flagged:  # if not flagged
                            flagged.append(mouse_grid_rect) # flag tile

                        else:                       # if  already flagged
                            flag_index = flagged.index(mouse_grid_rect)
                            del flagged[flag_index] # unflag

        draw_flags()

        # Draw the numbers on numbered squares that have been revealed
        if len(revealed) > 0:
            for square in revealed:
                txt = square[0]
                rect = square[1]
                WIN.blit(txt, rect)

        # Draw blank rect at the bottom to hide stuff and write text onto
        white_rect = pygame.Rect(
            0, GRID_HEIGHT_PX, 
            WIDTH, HEIGHT-GRID_HEIGHT_PX
            )
        pygame.draw.rect(WIN, WHITE, white_rect)

        # Get the time in seconds passed and draw to white area below grid
        ticks_passed += clock.get_time()
        seconds_passed = ticks_passed // 1000
        time_txt = COMICSANSMS.render(f"Time: {seconds_passed}", False, BLACK)
        WIN.blit(time_txt, (0, GRID_HEIGHT_PX))

        # Get the number of flags and mines and draw to white area below grid
        num_flags = COMICSANSMS.render(
            f"Flagged: {len(flagged)}", False, BLACK
            )
        WIN.blit(num_flags, (0, GRID_HEIGHT_PX+25))
        mines_txt = COMICSANSMS.render(f"Mines: {len(MINES)}", False, BLACK)
        WIN.blit(mines_txt, (0, GRID_HEIGHT_PX+50))

        # Check if all flagged are all bombs
        if sorted(flagged) == sorted(MINES):
            # Draw large win screen text to white area below grid
            COMICSANSMSWIN = pygame.font.SysFont("comicsansms", 36)
            win_text = COMICSANSMSWIN.render("You win!", False, BLACK)
            WIN.blit(win_text, (WIDTH//2-50, GRID_HEIGHT_PX+50))
            pygame.display.update()
            pygame.time.wait(2000)
            pygame.quit()
            sys.exit()

        # Pygame display and clock regulation
        pygame.display.update()
        clock.tick(12)


if __name__ == "__main__":
    main()