# Pygame template for new games
from Sprites import *
import pygame as pg
import random
from settings import *
from os import path
import sys

main_menu = True
game_over = True


class Game:

    def __init__(self):
        # initializes game window
        pg.init()  # starts the game
        pg.mixer.init()  # used for sound and music
        self.snd_list = []
        self.PREFERENCES = struc_Preferences()
        self.screen = pg.display.set_mode((WIDTH, HEIGHT))
        pg.display.set_caption("Screen Scroller")
        self.clock = pg.time.Clock()
        self.running = True
        self.load_data()
        self.font_name = pg.font.match_font(FONT_NAME)

    def load_data(self):
        self.dir = path.dirname(__file__)
        img_dir = path.join(self.dir, 'img')
        with open(path.join(self.dir, HS_FILE), 'r+') as f:  # 'r+' creates and reads and writes a file
            try:
                self.highscore = int(f.read())
            except:
                self.highscore = 0

        self.spritesheet = Spritesheet(path.join(img_dir, SPRITESHEET))

        # CLOUD IMG
        self.cloud_images = []
        for i in range(1, 4):
            self.cloud_images.append(pg.image.load(path.join(img_dir, 'cloud{}.png'.format(i))).convert())

        # Load sound
        self.snd_dir = path.join(self.dir, 'snd')

        pg.mixer.music.load(path.join(self.snd_dir, 'wind.ogg'))

        self.jump_sound = self.add_sound(path.join(self.snd_dir, 'Jump10.wav'))
        self.death_sound = self.add_sound(path.join(self.snd_dir, 'Explosion4.wav'))
        self.score_sound = self.add_sound(path.join(self.snd_dir, 'Pickup_Coin4.wav'))
        self.adjust_sound()

    def add_sound(self, file_address):

        new_sound = pg.mixer.Sound(file_address)

        self.snd_list.append(new_sound)

        return new_sound

    def adjust_sound(self):

        for sound in self.snd_list:
            sound.set_volume(self.PREFERENCES.vol_effects)

        pg.mixer.music.set_volume(self.PREFERENCES.vol_music)

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

    def button(self, msg, x, y, w, h, ic, ac, size, action=None):
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
                    self.menu_main_options()
                elif action == "Play Again":
                    game_over = False
                    self.running = True
                elif action == "Save Options":
                    main_menu = False
                elif action == "Quit":
                    pg.quit()
                    quit()

        else:
            pg.draw.rect(self.screen, ic, (x, y, w, h))

        self.text(msg, size, BLACK, (x + (w / 2)), (y + (h * 1 / 3)))

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
            self.button("Play", 190, 350, 100, 50, GREEN, RED, 22, "Play")

            # Options BUTTON
            self.button("Options", 190, 410, 100, 50, GREEN, RED, 22, "Options")

            # Quit BUTTON
            self.button("Quit", 190, 470, 100, 50, GREEN, RED, 22, "Quit")

            pg.display.flip()

    def show_go_screen(self):
        # Game over screen
        global game_over

        self.HS_checker()

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

            if self.NHS == True:
                self.text("NEW HIGH SCORE!", 30, BLACK, WIDTH / 2 + 5, HEIGHT / 2 + 40)

            if self.NHS != True:
                self.text("High Score: " + str(self.highscore), 22, BLACK, WIDTH / 2, HEIGHT / 2 + 40)

            # Buttons
            self.button("Play Again", 190, 400, 100, 50, GREEN, RED, 21, "Play Again")
            self.button("Options", 190, 460, 100, 50, GREEN, RED, 22, "Options")
            self.button("Quit", 190, 520, 100, 50, GREEN, RED, 22, "Quit")

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

    def menu_main_options(self):

        # MENU VARS #
        setting_menu_width = 200
        setting_menu_height = 200
        settings_menu_bgcolor = GRAY

        # SLIDER VARS #
        slider_x = WIDTH / 2
        sound_effects_slider_y = 400
        sound_music_slider_y = sound_effects_slider_y + 50
        sound_effect_vol = 0.5

        text_y_offset = 26
        effects_text_y = sound_effects_slider_y - text_y_offset
        music_text_y = sound_music_slider_y - text_y_offset

        window_center = (WIDTH / 2, HEIGHT / 2)

        settings_menu_surface = pg.Surface((setting_menu_width,
                                            setting_menu_height))

        settings_menu_rect = pg.Rect(0,0,
                                    setting_menu_width,
                                    setting_menu_height - 300)

        settings_menu_rect.center = window_center

        menu_close = False

        sound_effect_slider = ui_slider(self.screen,
                                        (125, 15),
                                        (slider_x, sound_effects_slider_y),
                                        RED, GREEN,
                                        self.PREFERENCES.vol_effects)

        sound_music_slider = ui_slider(self.screen,
                                        (125, 15),
                                        (slider_x, sound_music_slider_y),
                                        RED, GREEN,
                                        self.PREFERENCES.vol_music)

        while not menu_close:

            for event in pg.event.get():
                if event.type == pg.QUIT:
                    pg.quit()
                    self.running = False
                if event.type == pg.KEYDOWN:
                    if event.key == pg.K_ESCAPE:
                        menu_close = True

            list_of_events = pg.event.get()
            mouse_pos = pg.mouse.get_pos()

            game_input = (list_of_events, mouse_pos)

            # EXIT #

            sound_effect_slider.update(game_input)
            sound_music_slider.update(game_input)

            settings_menu_surface.fill(settings_menu_bgcolor)

            self.screen.blit(settings_menu_surface, settings_menu_rect.topleft)

            self.button("Save", 190, 500, 100, 50,
                        GRAY, LT_GRAY, 22, "Save Options")

            self.text("Effects", 22, BLACK, slider_x, effects_text_y)

            self.text("Music", 22, BLACK, slider_x, music_text_y)

            current_effects_vol = self.PREFERENCES.vol_effects
            current_music_vol = self.PREFERENCES.vol_music

            sound_effect_slider.draw()
            sound_music_slider.draw()

            if current_effects_vol is not sound_effect_slider.current_val:
                self.PREFERENCES.vol_effects = sound_effect_slider.current_val
                self.adjust_sound()

            if current_music_vol is not sound_music_slider.current_val:
                self.PREFERENCES.vol_music = sound_music_slider.current_val
                self.adjust_sound()

            pg.display.flip()
        pg.display.flip()

    def HS_checker(self):
        # High score checker
        if self.score > self.highscore:
            self.highscore = self.score
            self.NHS = True
            with open(path.join(self.dir, HS_FILE), 'w') as f:
                f.write(str(self.highscore))
        else:
            self.NHS = False

    def pause(self):

        self.paused = True

        for event in pg.event.get():
            if event.type == pg.QUIT:
                self.running = False
                pg.quit()
                quit()






class ui_slider:

    def __init__(self, surface, size, center_coords, bg_color, fg_color, parameter_value):

        self.surface = surface
        self.size = size
        self.bg_color = bg_color
        self.fg_color = fg_color
        self.current_val = parameter_value

        self.bg_rect = pg.Rect((0,0), size)
        self.bg_rect.center = center_coords
        self.fg_rect = pg.Rect((0, 0),
                               (self.bg_rect.w * self.current_val, self.bg_rect.h))
        self.fg_rect.topleft = self.bg_rect.topleft

        self.grip_tab = pg.Rect((0, 0), (20, self.bg_rect.h + 4))
        self.grip_tab.center = (self.fg_rect.right, self.bg_rect.centery)

    def update(self, player_input):

        mouse_down = pg.mouse.get_pressed()[0]

        local_events, local_mousepos = player_input
        mouse_x, mouse_y = local_mousepos

        mouse_over = (mouse_x >= self.bg_rect.left
                       and mouse_x <= self.bg_rect.right
                       and mouse_y >= self.bg_rect.top
                       and mouse_y <= self.bg_rect.bottom)

        if mouse_down and mouse_over:
            self.current_val = (float(float(mouse_x) - float(self.bg_rect.left)) / self.bg_rect.width)

            self.fg_rect.width = self.bg_rect.width * self. current_val

            self.grip_tab.center = (self.fg_rect.right, self.bg_rect.centery)

    def draw(self):
        # Draws background rect #
        pg.draw.rect(self.surface, self.bg_color, self.bg_rect)
        # Draws foreground rect #
        pg.draw.rect(self.surface, self.fg_color, self.fg_rect)
        # Draws slider tab #
        pg.draw.rect(self.surface, BLACK, self.grip_tab)


class struc_Preferences:

    def __init__(self):

        self.vol_effects = 0.5
        self.vol_music = 0.5


g = Game()
g.show_start_screen()

while g.running:
    g.new()
    g.show_go_screen()

pg.quit()