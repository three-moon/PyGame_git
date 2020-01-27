import pygame
from random import choice
import sys
import os
import pygame_gui

WIDTH, HEIGHT = 1280, 720


class Snake:  # Класс змейки
    FPS = 5
    SIZE = 10
    COLOR = 'common'
    GOD = False

    def __init__(self):
        self.color = self.COLOR
        self.width = self.SIZE
        self.array = [(0, 0, 1)]
        self.head_x = 5
        self.head_y = 5
        self.left = 100
        self.top = 100
        self.cell_size = 500 // self.SIZE
        self.max_len = 1
        self.meal = (choice(range(self.width)), choice(range(self.width)))
        while self.meal in [(x, y) for (x, y, r) in self.array]:
            self.meal = (choice(range(self.width)), choice(range(self.width)))
        self.all_sprites = pygame.sprite.Group()

    def get_score(self):  # Получение счёта
        return self.max_len - 1

    def can_move(self, c):  # Проверка возможности перемещения
        if self.GOD:
            return True
        (x, y) = c
        if c in [(x, y) for (x, y, r) in self.array]:
            return False
        elif x >= self.width or y >= self.width or x < 0 or y < 0:
            return False
        else:
            return True

    def move(self, motion):  # Перемещение змейки
        (x, y, r1) = self.array[-1]
        r = -1
        if motion == 0:
            y -= 1
            if r1 == 1:
                r = 4
            elif r1 == 3:
                r = 5
            else:
                r = 0
        elif motion == 2:
            y += 1
            if r1 == 1:
                r = 7
            elif r1 == 3:
                r = 6
            else:
                r = 2
        elif motion == 3:
            x -= 1
            if r1 == 0:
                r = 7
            elif r1 == 2:
                r = 4
            else:
                r = 3
        elif motion == 1:
            x += 1
            if r1 == 0:
                r = 6
            elif r1 == 2:
                r = 5
            else:
                r = 1
        if self.can_move((x, y)):
            self.array[-1] = (*self.array[-1][:2], r)
            self.array.append((x, y, motion))
            if self.eat() == 2:
                return 2
            if len(self.array) > self.max_len:
                self.array = self.array[1:]
            return False
        else:
            return True

    def eat(self):  # Функция увеличения длины змейки и проверка выигрыша
        if self.array[-1][:2] == self.meal:
            self.max_len += 1
            if self.max_len >= self.width ** 2:
                return 2
            self.meal = (choice(range(self.width)), choice(range(self.width)))
            while self.meal in [(x, y) for (x, y, r) in self.array]:
                self.meal = (choice(range(self.width)), choice(range(self.width)))

    def render(self):  # Отрисовка змейки
        (x, y, r) = self.array[-1]
        Tile(self.all_sprites, self.left + self.cell_size * x, self.top + self.cell_size * y, self.cell_size, 'head',
             self.color, r)

        for c in self.array[:-1]:
            (x, y, r) = c
            if r < 4:
                Tile(self.all_sprites, self.left + self.cell_size * x, self.top + self.cell_size * y, self.cell_size,
                     'body', self.color, r)
            else:
                Tile(self.all_sprites, self.left + self.cell_size * x, self.top + self.cell_size * y, self.cell_size,
                     'angle', self.color, r - 4)
        (x, y) = self.meal
        Tile(self.all_sprites, self.left + self.cell_size * x, self.top + self.cell_size * y, self.cell_size, 'meal')

        self.all_sprites.draw(screen)
        self.all_sprites.update()


class Tile(pygame.sprite.Sprite):  # Класс тайла
    def __init__(self, group, x, y, cell_size, type, color=None, r=0):
        if color:
            fullname = os.path.join('data/' + color, type + '.png')
        else:
            fullname = os.path.join('data', type + '.png')
        Tile.image = pygame.image.load(fullname).convert_alpha()
        super().__init__(group)
        self.image = pygame.transform.scale(Tile.image, (cell_size, cell_size))
        if r:
            self.image = pygame.transform.rotate(self.image, -90 * r)
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y

    def update(self):  # Удаление спрайта
        self.kill()


def terminate():  # Закрытие игры
    pygame.quit()
    sys.exit()


def main_menu():  # Отрисовка главного меню
    intro_text = ['ИГРА "ЗМЕЙКА"']

    fon = pygame.transform.scale(load_image('fon.jpg'), (WIDTH, HEIGHT))
    screen.blit(fon, (0, 0))
    font = pygame.font.Font(None, 100)
    text_coord = 100
    for line in intro_text:
        string_rendered = font.render(line, 1, pygame.Color('white'))
        intro_rect = string_rendered.get_rect()
        text_coord += 10
        intro_rect.top = text_coord
        intro_rect.x = 375
        text_coord += intro_rect.height
        screen.blit(string_rendered, intro_rect)

    start_button = pygame_gui.elements.UIButton(relative_rect=pygame.Rect((390, 300), (500, 50)),
                                                text='НАЧАТЬ ИГРУ',
                                                manager=manager)
    settings_button = pygame_gui.elements.UIButton(relative_rect=pygame.Rect((390, 350), (500, 50)),
                                                   text='НАСТРОЙКИ',
                                                   manager=manager)
    exit_button = pygame_gui.elements.UIButton(relative_rect=pygame.Rect((390, 400), (500, 50)),
                                               text='ВЫХОД',
                                               manager=manager)

    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                terminate()
            elif event.type == pygame.USEREVENT:
                if event.user_type == 'ui_button_pressed':
                    if event.ui_element == start_button:
                        start_button.kill()
                        settings_button.kill()
                        exit_button.kill()
                        return
                    elif event.ui_element == settings_button:
                        start_button.kill()
                        settings_button.kill()
                        exit_button.kill()
                        return settings()
                    elif event.ui_element == exit_button:
                        terminate()

            manager.process_events(event)

        manager.update(time_delta)

        manager.draw_ui(screen)
        pygame.display.flip()
        clock.tick(60)


def game():  # Главный игровой цикл
    snake = Snake()
    running = True
    motion = -1
    fon = pygame.transform.scale(load_image('game_fon.jpg'), (WIDTH, HEIGHT))
    while running:
        clock.tick(Snake.FPS)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                terminate()
            if event.type == pygame.KEYDOWN:
                _return = 0
                if event.key == pygame.K_LEFT:
                    motion = 3
                elif event.key == pygame.K_RIGHT:
                    motion = 1
                elif event.key == pygame.K_UP:
                    motion = 0
                elif event.key == pygame.K_DOWN:
                    motion = 2
                elif event.key == pygame.K_BACKQUOTE:
                    if snake.GOD:
                        snake.GOD = False
                        print('God mode disabled')
                    else:
                        snake.GOD = True
                        print('God mode activated')
        screen.blit(fon, (0, 0))
        flag = snake.move(motion)
        if flag and motion != -1:
            if flag == 2:
                return game_end(-1)
            else:
                return game_end(snake.get_score())
        snake.render()
        draw_score(snake.get_score())
        pygame.display.flip()


def settings():  # Отрисовка экрана настроек
    fon = pygame.transform.scale(load_image('fon.jpg'), (WIDTH, HEIGHT))
    screen.blit(fon, (0, 0))
    font = pygame.font.Font(None, 60)
    size_top = 100
    color_top = 100
    speed_top = 300
    size_fon = pygame.Surface((500, 50))
    size_fon.fill((255, 255, 255))
    color_fon = pygame.Surface((500, 100))
    color_fon.fill((255, 255, 255))
    speed_fon = pygame.Surface((500, 50))
    speed_fon.fill((255, 255, 255))
    board_size = Snake.SIZE
    color = Snake.COLOR
    speed = Snake.FPS
    all_sprites = pygame.sprite.Group()
    string_rendered = font.render('НАСТРОЙКИ', 1, pygame.Color('white'))
    intro_rect = string_rendered.get_rect()
    intro_rect.top = 10
    intro_rect.x = 515
    screen.blit(string_rendered, intro_rect)

    string_rendered = font.render('Размеры поля: ' + str(board_size), 1,
                                  pygame.Color('black'))
    intro_rect = string_rendered.get_rect()
    intro_rect.top = size_top
    intro_rect.x = 10
    screen.blit(size_fon, (10, size_top))
    screen.blit(string_rendered, intro_rect)

    string_rendered = font.render('Скоресть игры: ' + str(board_size) + '*' + str(board_size), 1,
                                  pygame.Color('black'))
    intro_rect = string_rendered.get_rect()
    intro_rect.top = size_top
    intro_rect.x = 10
    screen.blit(size_fon, (10, size_top))
    screen.blit(string_rendered, intro_rect)

    string_rendered = font.render('Цвет змейки:', 1, pygame.Color('black'))
    intro_rect = string_rendered.get_rect()
    intro_rect.top = size_top
    intro_rect.x = 770
    screen.blit(color_fon, (770, color_top))
    screen.blit(string_rendered, intro_rect)

    size_slider = pygame_gui.elements.ui_horizontal_slider.UIHorizontalSlider(
        relative_rect=pygame.Rect((10, size_top + 50), (500, 50)),
        start_value=board_size,
        value_range=(2, 25),
        manager=manager)
    speed_slider = pygame_gui.elements.ui_horizontal_slider.UIHorizontalSlider(
        relative_rect=pygame.Rect((10, speed_top + 50), (500, 50)),
        start_value=speed,
        value_range=(1, 60),
        manager=manager)
    exit_button = pygame_gui.elements.UIButton(relative_rect=pygame.Rect((390, 500), (500, 100)),
                                               text='ВЫХОД В МЕНЮ',
                                               manager=manager)
    common_button = pygame_gui.elements.UIButton(relative_rect=pygame.Rect((770, 200), (500, 50)),
                                                 text='ОБЫЧНЫЙ',
                                                 manager=manager)
    red_button = pygame_gui.elements.UIButton(relative_rect=pygame.Rect((770, 250), (500, 50)),
                                              text='КРАСНЫЙ',
                                              manager=manager)
    blue_button = pygame_gui.elements.UIButton(relative_rect=pygame.Rect((770, 300), (500, 50)),
                                               text='СИНИЙ',
                                               manager=manager)
    green_button = pygame_gui.elements.UIButton(relative_rect=pygame.Rect((770, 350), (500, 50)),
                                                text='ЗЕЛЁНЫЙ',
                                                manager=manager)
    while True:
        board_size = round(size_slider.get_current_value())
        string_rendered = font.render('Размеры поля: ' + str(board_size) + '*' + str(board_size), 1,
                                      pygame.Color('black'))
        intro_rect = string_rendered.get_rect()
        intro_rect.top = size_top
        intro_rect.x = 10
        screen.blit(size_fon, (10, size_top))
        screen.blit(string_rendered, intro_rect)

        speed = round(speed_slider.get_current_value())
        string_rendered = font.render('Скорость игры: ' + str(speed), 1,
                                      pygame.Color('black'))
        intro_rect = string_rendered.get_rect()
        intro_rect.top = speed_top
        intro_rect.x = 10
        screen.blit(speed_fon, (10, speed_top))
        screen.blit(string_rendered, intro_rect)

        Tile(all_sprites, 1170, 100, 100, 'head', color)

        all_sprites.draw(screen)
        all_sprites.update()
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                terminate()

            elif event.type == pygame.USEREVENT:
                if event.user_type == 'ui_button_pressed':
                    if event.ui_element == exit_button:
                        exit_button.kill()
                        size_slider.kill()
                        speed_slider.kill()
                        common_button.kill()
                        red_button.kill()
                        blue_button.kill()
                        green_button.kill()
                        Snake.SIZE = board_size
                        Snake.COLOR = color
                        Snake.FPS = speed
                        return main_menu()
                    if event.ui_element == common_button:
                        color = 'common'
                    if event.ui_element == red_button:
                        color = 'red'
                    if event.ui_element == blue_button:
                        color = 'blue'
                    if event.ui_element == green_button:
                        color = 'green'

            manager.process_events(event)

        manager.update(time_delta)

        manager.draw_ui(screen)
        pygame.display.flip()
        clock.tick(60)


def game_end(score):  # Отрисовка экрана результатов игры
    if score == -1:
        intro_text = ["ВЫ ПОБЕДИЛИ"]
    else:
        intro_text = ["ВЫ ПРОИГРАЛИ", "СЧЁТ: " + str(score)]
    fon = pygame.transform.scale(load_image('fon.jpg'), (WIDTH, HEIGHT))
    screen.blit(fon, (0, 0))
    font = pygame.font.Font(None, 100)
    text_coord = 50
    for line in intro_text:
        string_rendered = font.render(line, 1, pygame.Color('white'))
        intro_rect = string_rendered.get_rect()
        text_coord += 10
        intro_rect.top = text_coord
        intro_rect.x = 50
        text_coord += intro_rect.height
        screen.blit(string_rendered, intro_rect)

    exit_menu_button = pygame_gui.elements.UIButton(relative_rect=pygame.Rect((390, 500), (500, 100)),
                                                    text='ВЫХОД В МЕНЮ',
                                                    manager=manager)
    exit_windows_button = pygame_gui.elements.UIButton(relative_rect=pygame.Rect((390, 600), (500, 100)),
                                                       text='ВЫХОД ИЗ ИГРЫ',
                                                       manager=manager)
    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                terminate()
            elif event.type == pygame.USEREVENT:
                if event.user_type == 'ui_button_pressed':
                    if event.ui_element == exit_menu_button:
                        exit_menu_button.kill()
                        exit_windows_button.kill()
                        return main_menu()
                    elif event.ui_element == exit_windows_button:
                        terminate()
            manager.process_events(event)

        manager.update(time_delta)
        manager.draw_ui(screen)
        pygame.display.flip()
        clock.tick(60)


def load_image(name, colorkey=None):  # Загрузка изображений
    fullname = os.path.join('data', name)
    image = pygame.image.load(fullname)
    if colorkey is not None:
        if colorkey == -1:
            colorkey = image.get_at((0, 0))
        image.set_colorkey(colorkey)
    else:
        image = image.convert_alpha()
    return image


def draw_score(score):  # Отрисовка счёта во время игры
    font = pygame.font.Font(None, 100)
    string_rendered = font.render("СЧЁТ: " + str(score), 1, pygame.Color('white'))
    intro_rect = string_rendered.get_rect()
    intro_rect.top = 175
    intro_rect.x = 850
    screen.blit(string_rendered, intro_rect)


size = WIDTH, HEIGHT
screen = pygame.display.set_mode(size)
pygame.init()
pygame.display.set_caption('Змейка')
clock = pygame.time.Clock()
time_delta = clock.tick(60) / 1000.0
manager = pygame_gui.UIManager(size)

main_menu()
while True:
    game()

pygame.quit()
