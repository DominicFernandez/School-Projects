# Pygame template for new games
from Sprites import *
import pygame as pg
import random
from settings import *
from os import path


class Game:
    def __init__(self):
        #initializes game window
        pg.init()  # starts the game
        pg.mixer.init()  # used for sound and music
        self.screen = pg.display.set_mode((WIDTH, HEIGHT))
        pg.display.set_caption("Screen Scroller")
        self.clock = pg.time.Clock()
        self.running = True
        self.font_name = pg.font.match_font(FONT_NAME)
        self.load_data()

    def load_data(self):
        self.dir = path.dirname(__file__)
        with open(path.join(self.dir, HS_FILE), 'r+') as f:  # 'r+' creates and reads and writes a file
            try:
                self.highscore = int(f.read())
            except:
                self.highscore = 0

    def new(self):
        #Start a new game
        self.score = 0
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
                    self.score += 1

        while len(self.platforms) < 6:
            pwidth = random.randrange(50, 100)
            p = Platform(random.randrange(0, WIDTH - pwidth),
                         random.randrange(-45, -35),
                         pwidth, 20, GREEN)
            self.platforms.add(p)
            self.all_sprites.add(p)
        #DEATH
        if self.player.rect.bottom > HEIGHT:
            for sprite in self.all_sprites:
                sprite.rect.y -= max(self.player.vel.y, 10)
                if sprite.rect.bottom < 0:
                    sprite.kill()

        if len(self.platforms) == 0:
            self.playing = False

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
        self.screen.fill(BG_COLOR)
        self.all_sprites.draw(self.screen)
        self.text(str(self.score), 24, BLACK, WIDTH / 2, 20)
        pg.display.flip()

    def show_start_screen(self):
        #Game start menu
        self.screen.fill(BG_COLOR)
        self.text("Jump Man", 45, WHITE, WIDTH / 2, HEIGHT /4)
        self.text("High Score: " + str(self.highscore), 22, WHITE, WIDTH / 2, HEIGHT * 2 / 5)
        self.text("A, D, and SPACE to move", 22, WHITE, WIDTH / 2, HEIGHT / 2)
        self.text("Press any key to start", 22, WHITE, WIDTH / 2, HEIGHT * 3 / 4)
        pg.display.flip()
        self.key_wait()

    def show_go_screen(self):
        #Gameover screen
        if not self.running:
            return
        self.screen.fill(BG_COLOR)
        self.text("GAME OVER", 45, WHITE, WIDTH / 2, HEIGHT / 4)
        self.text("Score: " + str(self.score), 22, WHITE, WIDTH / 2, HEIGHT / 2)
        self.text("Press any key to play again", 22, WHITE, WIDTH / 2, HEIGHT * 3 / 4)
        if self.score > self.highscore:
            self.highscore = self.score
            self.text("NEW HIGH SCORE!", 30, WHITE, WIDTH / 2, HEIGHT / 2 - 30)
            with open(path.join(self.dir, HS_FILE), 'w') as f:
                f.write(str(self.highscore))
        else:
            self.text("High Score: " + str(self.highscore), 22, WHITE, WIDTH / 2, HEIGHT / 2 + 40)

        pg.display.flip()
        self.key_wait()

    def key_wait(self):
        waiting = True
        while waiting:
            self.clock.tick(FPS)
            for event in pg.event.get():
                if event.type == pg.QUIT:
                    waiting = False
                    self.running = False
                if event.type == pg.KEYUP:
                    waiting = False

    def text(self, text, size, color, x, y):
        font = pg.font.Font(self.font_name, size)
        text_surface = font.render(text, True, color)
        text_rect = text_surface.get_rect()
        text_rect.midtop = (x, y)
        self.screen.blit(text_surface,text_rect)

g = Game()
g.show_start_screen()

while g.running:
    g.new()
    g.show_go_screen()

pg.quit()