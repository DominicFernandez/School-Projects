#Sprites classes for game
from settings import *
import pygame as pg
import os
vec = pg.math.Vector2

class Player(pg.sprite.Sprite):
    def __init__(self):
        pg.sprite.Sprite.__init__(self)
        #self.image = pg.image.load(os.path.join(img, "p1_jump.png")).convert()
        self.image = pg.Surface((30, 40))
        self.image.fill(YELLOW)
        self.rect = self.image.get_rect()
        self.rect.center = (WIDTH / 2, HEIGHT / 2)
        self.pos = vec(WIDTH / 2, HEIGHT / 2)
        self.vel = vec(0, 0)
        self.acc = vec(0, 0)

    def update(self):
        self.acc = vec(0, 0)
        keys = pg.keys.get_pressed()
        if keys[pg.K_LEFT]:
            self.acc.x = -0.5
        if keys[pg.K_RIGHT]:
            self.acc.x = 0.5

        self.vel += self.acc
        self.pos += self.vel + 0.5 * self.acc