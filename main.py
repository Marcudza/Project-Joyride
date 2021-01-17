import os
import sys

import pygame
import pygame_gui

DISPLAY_SIZE = (1200, 667)
pygame.init()
playing = False
all_sprites = pygame.sprite.Group()
bomb_pos = None
jump = False
screen = pygame.display.set_mode(DISPLAY_SIZE)
manager = pygame_gui.UIManager(DISPLAY_SIZE)


def terminate():
    pygame.quit()
    sys.exit()


def load_image(name, colorkey=None):
    # если файл не существует, то выходим
    if not os.path.isfile(name):
        print(f"Файл с изображением '{name}' не найден")
        sys.exit()
    image = pygame.image.load(name)
    if colorkey is not None:
        image = image.convert()
        if colorkey == -1:
            colorkey = image.get_at((0, 0))
        image.set_colorkey(colorkey)
    else:
        image = image.convert_alpha()
    return image


def init_ui():
    fon = pygame.transform.scale(load_image('jetpack-joyride.jpg'), DISPLAY_SIZE)
    screen.blit(fon, (0, 0))
    new_game_button = pygame_gui.elements.UIButton(relative_rect=pygame.Rect((170, 570), (200, 50)),
                                                   text='Новая игра',
                                                   manager=manager)
    quit_button = pygame_gui.elements.UIButton(relative_rect=pygame.Rect((830, 570), (200, 50)),
                                               text='Выйти из игры',
                                               manager=manager)
    return new_game_button, quit_button


class AnimatedSprite(pygame.sprite.Sprite):
    def __init__(self, sheet, columns, rows, x, y):
        super().__init__(all_sprites)
        self.frames = []
        self.cut_sheet(sheet, columns, rows)
        self.cur_frame = 0
        self.image = self.frames[self.cur_frame]
        self.rect = self.rect.move(x, y)
        self.init_x = x
        self.init_y = y
        self.counter = 0
        self.jump_height = 300
        self.jump_up = True

    def cut_sheet(self, sheet, columns, rows):
        self.rect = pygame.Rect(0, 0, sheet.get_width() // columns,
                                sheet.get_height() // rows)
        for j in range(rows):
            for i in range(columns):
                frame_location = (self.rect.w * i, self.rect.h * j)
                self.frames.append(sheet.subsurface(pygame.Rect(
                    frame_location, self.rect.size)))

    def update(self):
        global playing, jump
        self.counter += 1
        if jump:

            if self.jump_up:
                self.jump_height -= 4
                self.rect.y -= 4
            else:
                self.jump_height += 4
                self.rect.y += 4
            if self.jump_height == 0:
                self.jump_up = False
            if self.jump_height == 300:
                jump = False
                self.jump_up = True
        if self.counter % 10 == 0:
            fon = pygame.transform.scale(load_image('game_bg.jpg'), DISPLAY_SIZE)
            screen.blit(fon, (0, 0))
            self.cur_frame = (self.cur_frame + 1) % len(self.frames)
            self.image = self.frames[self.cur_frame]
        hero_pos_x = (self.rect.x, self.rect.x + self.image.get_width())
        hero_pos_y = (self.rect.y, self.rect.y + self.image.get_height())

        if bomb_pos and hero_pos_x[0] <= bomb_pos.x <= hero_pos_x[1] and playing:
            if hero_pos_y[0] <= bomb_pos.y <= hero_pos_y[1]:
                playing = False
                jump = False
                self.jump_up = True
                self.jump_height = 300
                self.rect.x = self.init_x
                self.rect.y = self.init_y
                fon = pygame.transform.scale(load_image('jetpack-joyride.jpg'), DISPLAY_SIZE)
                screen.blit(fon, (0, 0))


class Bomb(pygame.sprite.Sprite):

    def __init__(self, *group):
        super().__init__(*group)
        self.image = load_image("bomb.png")
        self.rect = self.image.get_rect()
        self.rect.x = 1200
        self.rect.y = 500
        self.counter = 0

    def update(self):
        global bomb_pos
        if not playing:
            self.rect.x = 1200
        if self.rect.x == -68:
            self.rect.x = 1200

        self.rect = self.rect.move(-4, 0)
        bomb_pos = self.rect


def start_screen():
    global playing, jump
    new_game_button, quit_button = init_ui()
    if __name__ == '__main__':

        running = True
        clock = pygame.time.Clock()
        hero = AnimatedSprite(load_image("main_ch.png"), 3, 2, 100, 480)
        Bomb(all_sprites)
        while running:
            time_delta = clock.tick(60) / 1000.0

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_SPACE and playing and not jump:
                        jump = True
                if event.type == pygame.USEREVENT:
                    if event.user_type == pygame_gui.UI_BUTTON_PRESSED:
                        if event.ui_element == new_game_button:
                            playing = True
                            fon = pygame.transform.scale(load_image('game_bg.jpg'), DISPLAY_SIZE)
                            screen.blit(fon, (0, 0))
                            new_game_button.hide()
                            quit_button.hide()

                        if event.ui_element == quit_button:
                            terminate()

                manager.process_events(event)
            if playing:
                all_sprites.draw(screen)
                all_sprites.update()
            else:
                new_game_button.show()
                quit_button.show()
                manager.update(time_delta)
                manager.draw_ui(screen)
            pygame.display.update()

        terminate()


start_screen()
