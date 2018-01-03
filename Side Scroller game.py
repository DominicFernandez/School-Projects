# Pygame template for new games

import pygame
import random
import os
from settings import *

pygame.init() # starts the game
pygame.mixer.init() # used for sound and music
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Screen Scroller")
clock = pygame.time.Clock()

#set up assests folders
game_folder = os.path.dirname(__file__)
img_folder = os.path.join(game_folder, "img")

class Player(pygame.sprite.Sprite):
    def __init__(self):
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.image.load(os.path.join(img_folder, "p1_walk04.png")).convert()
        self.rect = self.image.get_rect()
        self.rect.center = (WIDTH / 2, HEIGHT / 2)
        self.y_speed = 5

    def update(self):
        self.rect.x += 5
        self.rect.y += self.y_speed
        if self.rect.left > WIDTH:
            self.rect.right = 0
        if self.rect.bottom > HEIGHT - 200:
            self.y_speed = -5
        if self.rect.top < 200:
            self.y_speed = 5


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
    screen.fill(BLACK)
    all_sprites.draw(screen)
    pygame.display.flip()