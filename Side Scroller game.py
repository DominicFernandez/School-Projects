# Pygame template for new games

import pygame as pg
import random
import os
from settings import *
from Sprites import *

class Game:
    def __init__(self):
        #initializes game window
        pg.init()  # starts the game
        pg.mixer.init()  # used for sound and music
        self.screen = pg.display.set_mode((WIDTH, HEIGHT))
        pg.display.set_caption("Screen Scroller")
        self.clock = pg.time.Clock()
        self.running = True

    def new(self):
        #Start a new game
        self.all_sprites = pg.sprite.Group()
        self.player = Player()
        self.all_sprites.add(Player)
        self.run()

    def run(self):
        #Game Loop
        self.playing = True
        while self.playing:
            self.clock.tick(FPS)
            self.events()
            self.update()
            self.draw()


    def update(self):
        #Game Loop - Update
        self.all_sprites.update()

    def events(self):
        #Game Loop - events
        for event in pg.event.get():
            if event.type == pg.QUIT:
                if self.playing:
                    self.playing = False
                self.running = False

    def draw(self):
        #Game Loop - Draw
        self.screen.fill(BLACK)
        self.all_sprites.draw(self.screen)
        pg.display.flip()

    def show_start_screen(self):
        #Game start menu
        pass

    def show_go_screen(self):
        #Gameover screen
        pass


g = Game()
g.show_start_screen()

while g.running:
    g.new()
    g.show_go_screen()

pg.quit()