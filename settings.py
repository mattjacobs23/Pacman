from pygame.math import Vector2 as vec


# Screen settings
WIDTH, HEIGHT = 610, 670
TOP_BOTTOM_BUFFER = 50
MAZE_WIDTH, MAZE_HEIGHT = WIDTH - TOP_BOTTOM_BUFFER, HEIGHT - TOP_BOTTOM_BUFFER
CELL_WIDTH, CELL_HEIGHT = MAZE_WIDTH // 28, MAZE_HEIGHT // 30
FPS = 60


# Color settings
BLACK = (5.1, 8.5, 15)
RED = (208, 22, 22)
GREY = (107, 107, 107)
WHITE = (255, 255, 255)
PLAYER_COLOR = (190, 194, 15)

# Font settings
START_TEXT_SIZE = 20
START_FONT = 'arial black'

# Player settings
# PLAYER_START_POS = vec(1, 1)
