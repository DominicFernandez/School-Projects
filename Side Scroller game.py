# Pygame template for new games
from Sprites import *
import pygame as pg
import random
from settings import *


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
        self.platforms = pg.sprite.Group()
        self.player = Player(self)
        self.all_sprites.add(self.player)
        for plat in PLATFORM_LIST:
            p = Platform(*plat)
            self.all_sprites.add(p)
            self.platforms.add(p)

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
        if self.player.vel.y > 0:
            hits = pg.sprite.spritecollide(self.player, self.platforms, False)
            if hits:
                self.player.pos.y = hits[0].rect.top
                self.player.vel.y = 0

#       srcreen scroller
        if self.player.rect.top <= HEIGHT / 4:
            self.player.pos.y += abs(self.player.vel.y)
            for plat in self.platforms:
                plat.rect.y += abs(self.player.vel.y)
                if plat.rect.top >= HEIGHT:
                    plat.kill()

        while len(self.platforms) < 6:
            pwidth = random.randrange(50, 100)
            p = Platform(random.randrange(0, WIDTH - pwidth),
                         random.randrange(-45, -35),
                         pwidth, 20)
            self.platforms.add(p)
            self.all_sprites.add(p)


    def events(self):
        #Game Loop - events
        for event in pg.event.get():
            if event.type == pg.QUIT:
                if self.playing:
                    self.playing = False
                self.running = False

            if event.type == pg.KEYDOWN:
                if event.key == pg.K_SPACE:
                    self.player.jump()

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