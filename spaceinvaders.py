import pygame, sys
from pygame.locals import QUIT, KEYUP, K_q, KEYDOWN, K_LEFT, K_RIGHT, K_ESCAPE

pygame.init()

# Constants:
WINDOW_WIDTH = 640
WINDOW_HEIGHT = 480
FIELD_LEFT_EDGE = 20
FIELD_RIGHT_EDGE = WINDOW_WIDTH - 20

ALIEN_COLOR = (255, 255, 255)
ALIEN_TYPE_0 = 0
ALIEN_TYPE_1 = 1
ALIEN_TYPE_2 = 2
ALIEN_FIELD_WIDTH = 10
ALIEN_FIELD_HEIGHT = 5
ALIEN_X_SPACING = 30
ALIEN_Y_SPACING = 30
ALIEN_MOVE_EVERY = 3  # move 1 pixel every this many ticks
ALIEN_X_JUMP = 10
ALIEN_Y_JUMP = 10  # how many pixels down to move

PLAYER_WIDTH = 50
PLAYER_HEIGHT = 30
PLAYER_TOP = WINDOW_HEIGHT - 50
PLAYER_COLOR = (0, 255, 0)
PLAYER_SPEED = 5

BARRIER_WIDTH = 40
BARRIER_HEIGHT = 20
BARRIER_COLOR = (0, 0, 255)

BG_COLOR = (0, 0, 0)
TEXT_COLOR = (255, 255, 0)

FPS = 30
FPS_CLOCK = pygame.time.Clock()

# Create alien sprites:
ALIEN_0_SURFACE = pygame.Surface((8, 6))
ALIEN_1_SURFACE = pygame.Surface((11, 8))
ALIEN_2_SURFACE = pygame.Surface((12, 8))

# XY coordinates obtained from _extract_invader_bitmaps.py
ALIEN_0_PIXELS = ((0, 1), (0, 2), (0, 5), (1, 0), (1, 1), (1, 2), (1, 4), (2, 0), (2, 2), (2, 3), (2, 5), (3, 0), (3, 1), (3, 2), (3, 4), (4, 0), (4, 1), (4, 2), (4, 4), (5, 0), (5, 2), (5, 3), (5, 5), (6, 0), (6, 1), (6, 2), (6, 4), (7, 1), (7, 2), (7, 5))
ALIEN_1_PIXELS = ((0, 4), (0, 5), (0, 6), (1, 3), (1, 4), (2, 0), (2, 2), (2, 3), (2, 4), (2, 5), (2, 6), (3, 1), (3, 2), (3, 4), (3, 5), (3, 7), (4, 2), (4, 3), (4, 4), (4, 5), (4, 7), (5, 2), (5, 3), (5, 4), (5, 5), (6, 2), (6, 3), (6, 4), (6, 5), (6, 7), (7, 1), (7, 2), (7, 4), (7, 5), (7, 7), (8, 0), (8, 2), (8, 3), (8, 4), (8, 5), (8, 6), (9, 3), (9, 4), (10, 4), (10, 5), (10, 6))
ALIEN_2_PIXELS = ((0, 2), (0, 3), (0, 4), (1, 1), (1, 2), (1, 3), (1, 4), (1, 6), (2, 1), (2, 2), (2, 3), (2, 4), (2, 5), (2, 6), (2, 7), (3, 1), (3, 2), (3, 4), (3, 5), (3, 7), (4, 0), (4, 1), (4, 2), (4, 4), (4, 5), (5, 0), (5, 1), (5, 2), (5, 3), (5, 4), (5, 6), (6, 0), (6, 1), (6, 2), (6, 3), (6, 4), (6, 6), (7, 0), (7, 1), (7, 2), (7, 4), (7, 5), (8, 1), (8, 2), (8, 4), (8, 5), (8, 7), (9, 1), (9, 2), (9, 3), (9, 4), (9, 5), (9, 6), (9, 7), (10, 1), (10, 2), (10, 3), (10, 4), (10, 6), (11, 2), (11, 3), (11, 4))

for pixel_xy in ALIEN_0_PIXELS:
    ALIEN_0_SURFACE.set_at(pixel_xy, ALIEN_COLOR)
for pixel_xy in ALIEN_1_PIXELS:
    ALIEN_1_SURFACE.set_at(pixel_xy, ALIEN_COLOR)
for pixel_xy in ALIEN_2_PIXELS:
    ALIEN_2_SURFACE.set_at(pixel_xy, ALIEN_COLOR)

# Enlarge the alien sprites
RESIZE_SCALE = 2
ALIEN_0_SURFACE = pygame.transform.scale(ALIEN_0_SURFACE, (ALIEN_0_SURFACE.get_rect().width * RESIZE_SCALE, ALIEN_0_SURFACE.get_rect().height * RESIZE_SCALE))
ALIEN_1_SURFACE = pygame.transform.scale(ALIEN_1_SURFACE, (ALIEN_1_SURFACE.get_rect().width * RESIZE_SCALE, ALIEN_1_SURFACE.get_rect().height * RESIZE_SCALE))
ALIEN_2_SURFACE = pygame.transform.scale(ALIEN_2_SURFACE, (ALIEN_2_SURFACE.get_rect().width * RESIZE_SCALE, ALIEN_2_SURFACE.get_rect().height * RESIZE_SCALE))
ALIEN_MAX_WIDTH = max(ALIEN_0_SURFACE.get_rect().width, ALIEN_1_SURFACE.get_rect().width, ALIEN_2_SURFACE.get_rect().width)  # The width of the widest alien sprite.
ALIEN_MAX_HEIGHT = max(ALIEN_0_SURFACE.get_rect().height, ALIEN_1_SURFACE.get_rect().height, ALIEN_2_SURFACE.get_rect().height)  # The height of the tallest alien sprite.

ALIEN_Y_TO_SURFACE_MAPPING = {0: ALIEN_0_SURFACE, 1: ALIEN_1_SURFACE, 2: ALIEN_1_SURFACE, 3: ALIEN_2_SURFACE, 4: ALIEN_2_SURFACE}

def main():
    global DISPLAY_SURFACE

    pygame.display.set_caption('Space Invaders')
    DISPLAY_SURFACE = pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT))

    while True:
        show_start_screen()
        run_game()
    
def run_game():
    # Use a simple rectangle for the player sprite:
    player_surface = pygame.Surface((13, 5))
    player_surface.fill((0, 255, 0))

    # Create the field with barriers:
    field_surface = pygame.Surface((WINDOW_WIDTH, WINDOW_HEIGHT))
    gap_width = (WINDOW_WIDTH - BARRIER_WIDTH * 4) // 5
    pygame.draw.rect(field_surface, BARRIER_COLOR, (gap_width * 1 + BARRIER_WIDTH * 0, WINDOW_HEIGHT - 100, BARRIER_WIDTH, BARRIER_HEIGHT))
    pygame.draw.rect(field_surface, BARRIER_COLOR, (gap_width * 2 + BARRIER_WIDTH * 1, WINDOW_HEIGHT - 100, BARRIER_WIDTH, BARRIER_HEIGHT))
    pygame.draw.rect(field_surface, BARRIER_COLOR, (gap_width * 3 + BARRIER_WIDTH * 2, WINDOW_HEIGHT - 100, BARRIER_WIDTH, BARRIER_HEIGHT))
    pygame.draw.rect(field_surface, BARRIER_COLOR, (gap_width * 4 + BARRIER_WIDTH * 3, WINDOW_HEIGHT - 100, BARRIER_WIDTH, BARRIER_HEIGHT))

    # START OF THE GAME
    aliens = []
    for x in range(ALIEN_FIELD_WIDTH):
        for y in range(ALIEN_FIELD_HEIGHT):
            aliens.append({'rect': pygame.Rect(x * ALIEN_X_SPACING + FIELD_LEFT_EDGE, y * ALIEN_Y_SPACING + FIELD_LEFT_EDGE, ALIEN_MAX_WIDTH, ALIEN_MAX_HEIGHT),
                           'surface': ALIEN_Y_TO_SURFACE_MAPPING[y]})

    player_left = WINDOW_WIDTH // 2
    moving_direction = 'none'
    aliens_direction = 'right'
    ticks = 0
    while True: # Main game loop.
        # UPDATE GAME STATE:
        # Move aliens
        for alien in aliens:  # if the alien is alive
            if aliens_direction == 'right' and ticks % ALIEN_MOVE_EVERY == 0:
                alien['rect'].move_ip(ALIEN_X_JUMP, 0)
            elif aliens_direction == 'left' and ticks % ALIEN_MOVE_EVERY == 0:
                alien['rect'].move_ip(-ALIEN_X_JUMP, 0)

        # Check if aliens need to jump down and change direction
        if aliens_direction == 'right':
            if max([alien['rect'].right for alien in aliens]) > FIELD_RIGHT_EDGE:
                # jump down and change direction:
                aliens_direction = 'left'
                for alien in aliens:
                    alien['rect'].move_ip(0, ALIEN_Y_JUMP)
        elif aliens_direction == 'left':
            if min([alien['rect'].left for alien in aliens]) < FIELD_LEFT_EDGE:
                # jump down and change direction:
                aliens_direction = 'right'
                for alien in aliens:
                    alien['rect'].move_ip(0, ALIEN_Y_JUMP)
                    
        if max([alien['rect'].bottom for alien in aliens]) >= PLAYER_TOP:
            break  # exit game


        # Start with the field and barriers:
        DISPLAY_SURFACE.blit(field_surface, field_surface.get_rect())

        # Draw aliens
        for alien in aliens:  # if the alien is alive
            DISPLAY_SURFACE.blit(alien['surface'], alien['rect'])

        # Draw the player:
        pygame.draw.rect(DISPLAY_SURFACE, PLAYER_COLOR, (player_left, PLAYER_TOP, PLAYER_WIDTH, PLAYER_HEIGHT))

        # Get input to check for key press or quit event:
        exit_loop = False
        for event in pygame.event.get(QUIT):
            quit()
        for event in pygame.event.get():
            if event.type == KEYDOWN:
                if event.key == K_LEFT:
                    moving_direction = 'left'
                elif event.key == K_RIGHT:
                    moving_direction = 'right'
            elif event.type == KEYUP:
                if event.key == K_q or event.key == K_ESCAPE:
                    exit_loop = True
                elif event.key == K_LEFT and moving_direction == 'left':
                    moving_direction = 'none'
                elif event.key == K_RIGHT and moving_direction == 'right':
                    moving_direction = 'none'
        if exit_loop:
            break

        if moving_direction == 'left' and player_left > 0:
            player_left -= PLAYER_SPEED
        elif moving_direction == 'right' and (player_left + PLAYER_WIDTH) < WINDOW_WIDTH:
            player_left += PLAYER_SPEED
        elif moving_direction != 'none':
            moving_direction = 'none'

        # Render screen:
        pygame.display.update()
        FPS_CLOCK.tick(FPS)
        ticks += 1
    quit()


def show_start_screen():
    while True:  # Show start screen.
        DISPLAY_SURFACE.fill(BG_COLOR)

        # Draw the title and subtitle text:
        title_font = pygame.font.Font('freesansbold.ttf', 48)
        title_surf = title_font.render('Space Invaders', True, TEXT_COLOR)
        title_rect = title_surf.get_rect()
        title_rect.center = (WINDOW_WIDTH // 2, WINDOW_HEIGHT // 2)
        DISPLAY_SURFACE.blit(title_surf, title_rect)

        sub_font = pygame.font.Font('freesansbold.ttf', 16)
        sub_surf = sub_font.render('Press a key.', True, TEXT_COLOR)
        sub_rect = sub_surf.get_rect()
        sub_rect.center = (WINDOW_WIDTH // 2, WINDOW_HEIGHT // 2 + 100)
        DISPLAY_SURFACE.blit(sub_surf, sub_rect)

        # Get input to check for key press or quit event:
        exit_loop = False
        for event in pygame.event.get(QUIT):
            quit()
        for event in pygame.event.get():
            if event.type == KEYUP:
                exit_loop = True
        if exit_loop:
            break

        # Render screen:
        pygame.display.update()
        FPS_CLOCK.tick(FPS)
    

def quit():
    pygame.quit()
    sys.exit()


if __name__ == '__main__':
    main()