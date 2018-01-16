# Pygame template for new games
from Sprites import *
import pygame as pg
import random
from settings import *
from os import path

main_menu = True
game_over = True


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
        img_dir = path.join(self.dir, 'img')
        with open(path.join(self.dir, HS_FILE), 'r+') as f:  # 'r+' creates and reads and writes a file
            try:
                self.highscore = int(f.read())
            except:
                self.highscore = 0

        self.spritesheet = Spritesheet(path.join(img_dir, SPRITESHEET))

        #CLOUD IMG
        self.cloud_images = []
        for i in range(1, 4):
            self.cloud_images.append(pg.image.load(path.join(img_dir, 'cloud{}.png'.format(i))).convert())

        #Load sound
        self.snd_dir = path.join(self.dir, 'snd')

        self.jump_sound = pg.mixer.Sound(path.join(self.snd_dir, 'Jump10.wav'))

        self.death_sound = pg.mixer.Sound(path.join(self.snd_dir, 'Explosion4.wav'))
        self.score_sound = pg.mixer.Sound(path.join(self.snd_dir, 'Pickup_Coin4.wav'))

    def new(self):
        #Start a new game
        self.score = 0
        self.all_sprites = pg.sprite.LayeredUpdates()
        self.platforms = pg.sprite.Group()
        self.ppu = pg.sprite.Group()
        self.enemies = pg.sprite.Group()
        self.cloud = pg.sprite.Group()
        self.player = Player(self)
        for plat in PLATFORM_LIST:
            Platform(self, *plat)
        self.mob_timer = 0
        pg.mixer.music.load(path.join(self.snd_dir, 'wind.ogg'))
        pg.mixer.music.set_volume(0.3)
        for i in range(8):
            c = Cloud(self)
            c.rect.y += 580
        self.run()

    def run(self):
        #Game Loop
        pg.mixer.music.play(loops=-1)
        self.playing = True
        while self.playing:
            self.clock.tick(FPS)
            self.events()
            self.update()
            self.draw()
        pg.mixer.music.stop()

    def update(self):
        global game_over
        #Game Loop - Update
        self.all_sprites.update()

        #MOB SPAWNING
        now = pg.time.get_ticks()
        if now - self.mob_timer > 5000 + random.choice([-1000, -500, 0, 500, 1000]) and self.score > 25:
            self.mob_timer = now
            Enemy(self)

        #ENEMY Collision
        enemy_hits = pg.sprite.spritecollide(self.player, self.enemies, False, pg.sprite.collide_mask)
        if enemy_hits:
            self.death_sound.play()
            self.playing = False
            game_over = True

        if self.player.vel.y > 0:
            hits = pg.sprite.spritecollide(self.player, self.platforms, False)
            if hits:
                lowest = hits[0]
                for hit in hits:
                    if hit.rect.bottom > lowest.rect.bottom:
                        lowest = hit
                if self.player.pos.x < lowest.rect.right + 10 and self.player.pos.x > lowest.rect.left - 10:
                    if self.player.pos.y < lowest.rect.centery:
                        self.player.pos.y = hits[0].rect.top
                        self.player.vel.y = 0
                        self.player.jumping = False

#       screen scroller
        if self.player.rect.top <= HEIGHT / 4:
            if random.randrange(100) < 10:
                Cloud(self)
            for cloud in self.cloud:
                cloud.rect.y += max(abs(self.player.vel.y / random.randrange(2, 3)), 2)

            self.player.pos.y += max(abs(self.player.vel.y), 5)
            for enemy in self.enemies:
                enemy.rect.y += max(abs(self.player.vel.y), 5)
            for plat in self.platforms:
                plat.rect.y += max(abs(self.player.vel.y), 5)
                if plat.rect.top >= HEIGHT:
                    plat.kill()
                    self.score += 1

        #PPU hit
        Ppu_hits = pg.sprite.spritecollide(self.player, self.ppu, True)
        for ppu in Ppu_hits:
            if ppu.type == 'boost':
                self.player.vel.y = -BOOST_POWER
                self.player.jumping = False

        while len(self.platforms) < 5:
            pwidth = random.randrange(50, 100)
            Platform(self, random.randrange(0, WIDTH - pwidth),
                    random.randrange(-35, -30))
        #DEATH
        if self.player.rect.bottom > HEIGHT:
            for sprite in self.all_sprites:
                sprite.rect.y -= max(self.player.vel.y, 10)
                if sprite.rect.bottom < 0:
                    sprite.kill()
                    self.death_sound.play()
                    game_over = True


        if len(self.platforms) == 0:
            self.playing = False

        #score sound
        if self.score % 10 == 0 and self.score != 0:
            self.score_sound.play()
            self.score += 1

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

            if event.type == pg.KEYUP:
                if event.key == pg.K_SPACE:
                    self.player.jump_cut()

    def draw(self):
        #Game Loop - Draw
        self.screen.fill(BG_COLOR)
        self.all_sprites.draw(self.screen)
        self.text(str(self.score), 24, BLACK, WIDTH / 2, 20)
        pg.display.flip()

    def button(self, msg, x, y, w, h, ic, ac, action=None):
        global main_menu
        global game_over

        mouse = pg.mouse.get_pos()
        click = pg.mouse.get_pressed()

        if x + 100 > mouse[0] > x and y + 50 > mouse[1] > y:
            pg.draw.rect(self.screen, ac, (x, y, w, h))
            if click[0] == 1 and action != None:
                if action == "Play":
                    main_menu = False
                elif action == "Options":
                    pass
                elif action == "Play Again":
                    game_over = False
                    self.running = True
                elif action == "Quit":
                    pg.quit()
                    quit()

        else:
            pg.draw.rect(self.screen, ic, (x, y, w, h))

        self.text(msg, 22, BLACK, (x + (w / 2)), (y + (h / 4)))

    def show_start_screen(self):

        global main_menu

        while main_menu:
            for event in pg.event.get():
                if event.type == pg.QUIT:
                    self.running = False
                    pg.quit()
                    quit()

            # Game start menu
            self.screen.fill(BG_COLOR)
            self.text("Sky Stone", 45, BLACK, WIDTH / 2, HEIGHT /4)
            self.text("High Score: " + str(self.highscore), 22, BLACK, WIDTH / 2, HEIGHT * 2 / 5)
            self.text("A, D, and SPACE to move", 22, BLACK, WIDTH / 2, HEIGHT / 2)

            # BUTTONS
            # Play Button
            self.button("Play", 190, 350, 100, 50, DARK_GREEN, GREEN, "Play")

            # Options BUTTON
            self.button("Options", 190, 410, 100, 50, DARK_YELLOW, YELLOW, "Options")

            # Quit BUTTON
            self.button("Quit", 190, 470, 100, 50, DARK_RED, RED, "Quit")

            pg.display.flip()

    def show_go_screen(self):
        # Game over screen
        global game_over

        while game_over:
            for event in pg.event.get():
                if event.type == pg.QUIT:
                    self.running = False
                    pg.quit()
                    quit()

            if not self.running:
                return

            self.screen.fill(BG_COLOR)
            self.text("GAME OVER", 45, BLACK, WIDTH / 2, HEIGHT / 4)
            self.text("Score: " + str(self.score), 22, BLACK, WIDTH / 2, HEIGHT / 2)

            # High score checker
            if self.score > self.highscore:
                self.highscore = self.score
                self.text("NEW HIGH SCORE!", 30, BLACK, WIDTH / 2, HEIGHT / 2 - 30)
                with open(path.join(self.dir, HS_FILE), 'w') as f:
                    f.write(str(self.highscore))
            else:
                self.text("High Score: " + str(self.highscore), 22, BLACK, WIDTH / 2, HEIGHT / 2 + 40)

            # Buttons
            self.button("Play Again", 190, 400, 100, 50, DARK_GREEN, GREEN, "Play Again")
            self.button("Quit", 190, 460, 100, 50, DARK_RED, RED, "Quit")

            pg.display.flip()


    def key_wait(self):
        waiting = True
        while waiting:
            self.clock.tick(FPS)
            for event in pg.event.get():
                if event.type == pg.QUIT:
                    waiting = False
                    self.running = False
                if event.type == pg.KEYDOWN:
                    if event.key == pg.K_RETURN:
                        waiting = False

    def text(self, text, size, color, x, y):
        font = pg.font.Font(self.font_name, size)
        text_surface = font.render(text, True, color)
        text_rect = text_surface.get_rect()
        text_rect.midtop = (x, y)
        self.screen.blit(text_surface, text_rect)


g = Game()
g.show_start_screen()

while g.running:
    g.new()
    g.show_go_screen()

pg.quit()