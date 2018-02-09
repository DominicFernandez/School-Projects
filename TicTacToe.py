# Pygame template for new games

import pygame as pg
import random
from os import path

#Pygame settings
WIDTH = 480
HEIGHT = 600
FPS = 60


SPRITESHEET = ""

#Layers

#Colors
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
TRANSGRAY = (200, 200, 200, 128)


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
GRAY = (128, 128, 128)
LT_GRAY = (211, 211, 211)

BG_COLOR = BLUEGREEN

class Game:

    def __init__(self):
        # initializes game window
        pg.init()  # starts the game
        pg.mixer.init()  # used for sound and music
        self.screen = pg.display.set_mode((WIDTH, HEIGHT))
        pg.display.set_caption("TicTacToe vs AI")
        self.clock = pg.time.Clock()
        self.running = True
        self.load_data()

    def load_data(self):
        self.dir = path.dirname(__file__)
        img_dir = path.join(self.dir, 'img')
        self.font_name = path.join(img_dir, 'Soft Marshmallow.otf')

    def new(self):
        self.bWIDTH = 100
        self.bHEIGHT = 100

        self.screen.fill(WHITE)
        #pg.draw.rect(self.screen, RED, [87, 148, 310, 310])

        pg.draw.line(self.screen, BLACK, (189, HEIGHT / 2 - 152), (189, HEIGHT / 2 + 157), 5)
        pg.draw.line(self.screen, BLACK, (294, HEIGHT / 2 - 152), (294, HEIGHT / 2 + 157), 5)

        pg.draw.line(self.screen, BLACK, (WIDTH / 2 - 153, 250), (WIDTH / 2 + 157, 250), 5)
        pg.draw.line(self.screen, BLACK, (WIDTH / 2 - 153, 355), (WIDTH / 2 + 157, 355), 5)

        pg.draw.rect(self.screen, WHITE, [87, 148, self.bWIDTH, self.bHEIGHT])
        pg.draw.rect(self.screen, WHITE, [87, 253, self.bWIDTH, self.bHEIGHT])
        pg.draw.rect(self.screen, WHITE, [87, 358, self.bWIDTH, self.bHEIGHT])
        pg.draw.rect(self.screen, WHITE, [192, 148, self.bWIDTH, self.bHEIGHT])
        pg.draw.rect(self.screen, WHITE, [192, 253, self.bWIDTH, self.bHEIGHT])
        pg.draw.rect(self.screen, WHITE, [192, 358, self.bWIDTH, self.bHEIGHT])
        pg.draw.rect(self.screen, WHITE, [297, 148, self.bWIDTH, self.bHEIGHT])
        pg.draw.rect(self.screen, WHITE, [297, 253, self.bWIDTH, self.bHEIGHT])
        pg.draw.rect(self.screen, WHITE, [297, 358, self.bWIDTH, self.bHEIGHT])


        pg.display.flip()
        self.run()

    def run(self):
        self.playing = True
        self.player_turn = True
        while self.playing:
            self.clock.tick(FPS)
            self.events()

    def update(self):
        pass

    def events(self):

        for event in pg.event.get():
            if event.type == pg.QUIT:
                if self.playing:
                    self.playing = False
                self.running = False

        if self.player_turn == True:
            self.button("", 87, 148, 100, 100, WHITE, TRANSGRAY, 22, "Place")
            self.button("", 87, 253, 100, 100, WHITE, TRANSGRAY, 22, "Place")
            self.button("", 87, 358, 100, 100, WHITE, TRANSGRAY, 22, "Place")
            self.button("", 192, 148, 100, 100, WHITE, TRANSGRAY, 22, "Place")
            self.button("", 192, 253, 100, 100, WHITE, TRANSGRAY, 22, "Place")
            self.button("", 192, 358, 100, 100, WHITE, TRANSGRAY, 22, "Place")
            self.button("", 297, 148, 100, 100, WHITE, TRANSGRAY, 22, "Place")
            self.button("", 297, 253, 100, 100, WHITE, TRANSGRAY, 22, "Place")
            self.button("", 297, 358, 100, 100, WHITE, TRANSGRAY, 22, "Place")

            pg.display.flip()

    def button(self, msg, x, y, w, h, ic, ac, size, action=None):

        mouse = pg.mouse.get_pos()
        click = pg.mouse.get_pressed()

        if x + 100 > mouse[0] > x and y + 100 > mouse[1] > y:
            pg.draw.rect(self.screen, ac, (x, y, w, h))
            if click[0] == 1 and action != None:
                if action == "Place":
                    print("h")
                    self.player_turn = False
                    pg.draw.rect(self.screen, ic, (x, y, w, h))
        else:
            pg.draw.rect(self.screen, ic, (x, y, w, h))

            self.text(msg, size, BLACK, (x + (w / 2)), (y + (h * 1 / 3)))

    def text(self, text, size, color, x, y):
        font = pg.font.Font(self.font_name, size)
        text_surface = font.render(text, True, color)
        text_rect = text_surface.get_rect()
        text_rect.midtop = (x, y)
        self.screen.blit(text_surface, text_rect)

    def hover(self):
        while self.running:
            self.button("", 87, 148, 100, 100, GREEN, RED, 22, "Place")

            pg.display.flip()

g = Game()
while g.running:
    g.new()
    #g.show_go_screen()

pg.quit()
