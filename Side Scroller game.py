# Pygame template for new games

import pygame
import random

WIDTH = 360
HEIGHT = 480
FPS = 30

WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
RED = (255, 0, 0)
GREEN = (0, 255, 0)
BLUE = (0, 0, 255)
CYAN = (0, 255, 255)

class Player(pygame.sprite.Sprite):
    def __init__(self):
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.Surface((50, 50))
        self.image.fill(RED)
        self.rect = self.image.get_rect()
        self.rect.center = (WIDTH / 2, HEIGHT / 2)


pygame.init() # starts the game
pygame.mixer.init() # used for sound and music
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Screen Scroller")
clock = pygame.time.Clock()

all_sprites = pygame.sprite.Group()
player = Player()
all_sprites.add(player)

#Game loop
running = True
while running:
    clock.tick(FPS)
    #Process input (events)
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
    #Update
    all_sprites.update()
    #Draw / render
    screen.fill(CYAN)
    all_sprites.draw(screen)
    pygame.display.flip()