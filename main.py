import os
import sys

import pygame
import pygame_gui

DISPLAY_SIZE = (1200, 667)
pygame.init()
playing = False
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
    options_button = pygame_gui.elements.UIButton(relative_rect=pygame.Rect((390, 570), (200, 50)),
                                                  text='Настройки',
                                                  manager=manager)
    ladder_button = pygame_gui.elements.UIButton(relative_rect=pygame.Rect((610, 570), (200, 50)),
                                                 text='Таблица лидеров',
                                                 manager=manager)
    quit_button = pygame_gui.elements.UIButton(relative_rect=pygame.Rect((830, 570), (200, 50)),
                                               text='Выйти из игры',
                                               manager=manager)
    return new_game_button, options_button, ladder_button, quit_button


all_sprites = pygame.sprite.Group()


class AnimatedSprite(pygame.sprite.Sprite):
    def __init__(self, sheet, columns, rows, x, y):
        super().__init__(all_sprites)
        self.frames = []
        self.cut_sheet(sheet, columns, rows)
        self.cur_frame = 0
        self.image = self.frames[self.cur_frame]
        self.rect = self.rect.move(x, y)
        self.counter = 0

    def cut_sheet(self, sheet, columns, rows):
        self.rect = pygame.Rect(0, 0, sheet.get_width() // columns,
                                sheet.get_height() // rows)
        for j in range(rows):
            for i in range(columns):
                frame_location = (self.rect.w * i, self.rect.h * j)
                self.frames.append(sheet.subsurface(pygame.Rect(
                    frame_location, self.rect.size)))

    def update(self):
        self.counter += 1
        if self.counter % 10 == 0:
            fon = pygame.transform.scale(load_image('jetpack-joyride.jpg'), DISPLAY_SIZE)
            screen.blit(fon, (0, 0))
            self.cur_frame = (self.cur_frame + 1) % len(self.frames)
            self.image = self.frames[self.cur_frame]


class Bomb(pygame.sprite.Sprite):
    image = load_image("bomb.jpg", pygame.Color('white'))

    def __init__(self, *group):
        super().__init__(*group)
        self.image = Bomb.image
        self.rect = self.image.get_rect()
        self.rect.x = 1200
        self.rect.y = 480
        self.counter = 0

    def update(self):

        self.rect = self.rect.move(-1, self.rect.y)


def start_screen():
    global playing
    new_game_button, options_button, ladder_button, quit_button = init_ui()
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
                if event.type == pygame.USEREVENT:
                    if event.user_type == pygame_gui.UI_BUTTON_PRESSED:
                        if event.ui_element == new_game_button:
                            fon = pygame.transform.scale(load_image('game_bg.jpg'), DISPLAY_SIZE)
                            screen.blit(fon, (0, 0))
                            new_game_button.hide()
                            ladder_button.hide()
                            quit_button.hide()
                            playing = True
                        if event.ui_element == options_button:
                            fon = pygame.transform.scale(load_image('jetpack-joyride.jpg'), DISPLAY_SIZE)
                            screen.blit(fon, (0, 0))
                            new_game_button.show()
                            ladder_button.show()
                            quit_button.show()
                            playing = False
                        if event.ui_element == ladder_button:
                            print('Hello World!')
                        if event.ui_element == quit_button:
                            terminate()

                manager.process_events(event)

            all_sprites.draw(screen)
            all_sprites.update()
            manager.update(time_delta)
            manager.draw_ui(screen)
            pygame.display.update()

        terminate()


start_screen()
