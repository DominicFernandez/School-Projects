#Pygame settings
WIDTH = 480
HEIGHT = 600
FPS = 60
FONT_NAME = 'Comic Sans MS'
HS_FILE = "high score.txt"
SPRITESHEET = "spritesheet_jumper.png"

#player prop
PLAYER_ACC = 0.5
PLAYER_FRICTION = -0.12
PLAYER_GRAV = 0.8
PLAYER_JUMP = 22
MOB_FEQU = 5000

#Layers
PLAYER_LAY = 3
PLATFORM_LAY = 1
PPU_LAY = 2
ENEMY_LAY = 3
CLOUD_LAY = 0

#Boost settings
BOOST_POWER = 40
PPU_SPAWN_PCT = 5


#Colors
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)

RED = (255, 0, 0)
DARK_RED = (200, 0, 0)

YELLOW = (255, 255, 0)
DARK_YELLOW = (200, 200, 0)
GREEN = (0, 255, 0)
DARK_GREEN = (0, 200, 0)
BLUE = (0, 0, 255)
CYAN = (0, 255, 255)
PURPLE = (255, 0, 255)
DARKPURPLE = (51, 0, 51)
BLUEGREEN = (162, 247, 225)
BROWN = (51, 25, 0)


BG_COLOR = BLUEGREEN

#Starting Platforms
PLATFORM_LIST = [(0, HEIGHT - 35),
                 (0, HEIGHT - 20),
                 (WIDTH / 2 - 50, HEIGHT * 3 / 4),
                 (150, HEIGHT - 27),
                 (300, HEIGHT - 390),
                 (50, HEIGHT - 350),
                 (210, HEIGHT - 450)]