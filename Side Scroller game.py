# Pygame template for new games

import pygame
import random

WIDTH = 360
HEIGHT = 480
FPS = 30

pygame.init() # starts the game
pygame.mixer.init() # used for sound and music
screen = pygame.display.set_mode(WIDTH, HEIGHT)
pygame.display.set_caption("Screen Scroller")
clock = pygame.time.Clock()

#Game loop
running = True
while running:
    #Process input (events)
    #Update
    #Draw / render
    screen.fill(0, 255, 255)