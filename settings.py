#Pygame settings
WIDTH = 480
HEIGHT = 600
FPS = 60

#player prop
PLAYER_ACC = 0.5
PLAYER_FRICTION = -0.12
PLAYER_GRAV = 0.8
PLAYER_JUMP = 22

#Colors
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
RED = (255, 0, 0)
YELLOW = (255, 255, 0)
GREEN = (0, 255, 0)
BLUE = (0, 0, 255)
CYAN = (0, 255, 255)
PURPLE = (255, 0, 255)
DARKPURPLE = (51, 0, 51)

#Starting Platforms
PLATFORM_LIST = [(0, HEIGHT - 40, WIDTH, 40),
                 (WIDTH / 2 - 50, HEIGHT * 3 / 4, 100, 20),
                 (150, HEIGHT - 275, 50, 20),
                 (300, HEIGHT - 390, 100, 20),
                 (50, HEIGHT - 350, 100, 20),
                 (210, HEIGHT - 450, 100, 20)]