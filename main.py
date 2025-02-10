from time import sleep

import pygame
import os
from PIL import Image
import pickle

flag = False
scale = 1.0


pygame.init()
pygame.display.set_caption('Pink Panther: Old Friend')
os.chdir(f'{os.getcwd()}\\assets')
screen = pygame.display.set_mode((0, 0), pygame.FULLSCREEN)
screen_rect = pygame.Rect((0, 0), screen.get_size())
screen.fill('black')
pygame.display.update()
pygame.mixer.init()
clock = pygame.time.Clock()
intro_sprites = pygame.sprite.Group()

street_1 = pygame.sprite.Group()
street_2 = pygame.sprite.Group()
mansion_1 = pygame.sprite.Group()
mansion_2 = pygame.sprite.Group()
mansion_3 = pygame.sprite.Group()
mansion_4 = pygame.sprite.Group()
mansion_5 = pygame.sprite.Group()
mansion_6 = pygame.sprite.Group()

# intro(screen)
# menu(screen)

current_path = os.path.dirname(__file__)
assets_path = os.path.join(current_path, 'assets')


class AnimatedSprite(pygame.sprite.Sprite):
    def __init__(self, x, y, image_folder, frame_rate=10):
        super().__init__()

        self.frames = []
        for filename in sorted(os.listdir(image_folder)):
            if filename.endswith('.png'):
                frame = pygame.image.load(os.path.join(image_folder, filename))
                frame = pygame.transform.scale(frame, (500, 500))

                self.frames.append(frame)

        self.image = self.frames[0]
        self.rect = self.image.get_rect()

        self.current_frame = 0
        self.frame_rate = frame_rate
        self.clock = pygame.time.Clock()

        self.rect.x = x
        self.rect.y = y

    def get_coords(self):
        return self.rect.x, self.rect.y

    def update(self):
        self.current_frame = (self.current_frame + 1) % len(self.frames)
        self.image = self.frames[self.current_frame]


class Player(pygame.sprite.Sprite):
    def __init__(self, x, y, image_folder, scale=(150, 150)):
        super().__init__()

        self.scale = scale

        self.inventory = []

        self.frames = []
        for filename in sorted(os.listdir(image_folder)):
            if filename.endswith('.png'):
                frame = pygame.image.load(os.path.join(image_folder, filename))

                self.frames.append(frame)

        self.image = pygame.transform.scale(self.frames[0], self.scale)
        self.rect = self.image.get_rect()

        self.current_frame = 0
        self.clock = pygame.time.Clock()

        self.rect.x = x
        self.rect.y = y

        self.rect.clamp_ip(screen_rect)

    def check_borders(self):
        pass

    def get_coords(self):
        return self.rect.x, self.rect.y

    def update(self):
        self.current_frame = (self.current_frame + 1) % len(self.frames)
        self.image = pygame.transform.scale(self.frames[self.current_frame], self.scale)
        self.image = self.scale_image(self.image, scale)

    def moveForward(self):
        global scale
        self.frames = [pygame.image.load(os.path.join(f'{os.curdir}/icons', file)) for file in
                       os.listdir(f'{os.curdir}/icons') if 'forward' in file]
        if scale <= 1.5:
            scale += 0.01
        self.rect.y += 5

    def moveBack(self):
        global scale
        self.frames = [pygame.image.load(os.path.join(f'{os.curdir}/icons', file)) for file in
                       os.listdir(f'{os.curdir}/icons') if 'back' in file]
        if scale > 0.25:
            scale -= 0.01
        self.rect.y -= 5

    def moveRight(self):
        self.frames = [pygame.image.load(os.path.join(f'{os.curdir}/icons', file)) for file in
                       os.listdir(f'{os.curdir}/icons') if 'right' in file]
        self.rect.x += 5

    def moveLeft(self):
        self.frames = [pygame.image.load(os.path.join(f'{os.curdir}/icons', file)) for file in
                       os.listdir(f'{os.curdir}/icons') if 'left' in file]
        self.rect.x -= 5

    def standStraight(self):
        self.frames = [pygame.image.load(os.path.join(f'{os.curdir}/icons', file)) for file in
                       os.listdir(f'{os.curdir}/icons') if 'stand' in file]

    def scale_image(self, image, scale):
        return pygame.transform.scale(image, (int(image.get_width() * scale), int(image.get_height() * scale)))

    def add_item(self, item):
        self.inventory.append(item)

ply = Player(860, 910, os.path.join(f'{os.curdir}/icons'), (180, 180))


def sprite_groups_manager(group, list_of_sprites):
    for i in list_of_sprites:
        group.add(i)
    return group


def level_manager(level, transi=None):
    global flag
    global current_map
    global ply
    if level.level_name() == 'start_street_1':
        current_map = list_of_levels['start_street_2']
        return
    elif level.level_name() == 'start_street_2':
        current_map = list_of_levels['mansion_1']
        return
    elif level.level_name() == 'mansion_1':
        ply.scale = (300, 300)
        current_map = list_of_levels['mansion_2']
        return
    elif level.level_name() == 'mansion_2':
        current_map = list_of_levels['mansion_3']
        return
    elif level.level_name() == 'mansion_3':
        current_map = list_of_levels['mansion_4']
        return
    # elif level.level_name() == 'mansion_4':
    #     current_map = list_of_levels['man']
    #     return


class Item(pygame.sprite.Sprite):
    def __init__(self, name, image):
        super().__init__()

        self.name = name
        self.image = pygame.image.load(image)
        image_rect = self.image.get_rect()

    def get_name(self):
        return self.name

    def image_for_ui(self):
        return self.image


list_of_items = {

    'Candle': Item('Свечка', os.path.join(assets_path, 'candle.png')),

    'Key': Item('Ключ', os.path.join(assets_path, 'key.png')),
}


class InventoryUI:
    def __init__(self, items=None, width=80, height=700, scale=(50, 50), enabled=False):
        self.width = width
        self.height = height
        self.items = items
        self.scale = scale
        self.font = pygame.font.Font(None, 36)
        self.rect = pygame.Rect(50, 50, height, width)

        self.enabled = enabled

    def movement_collision(self, coords):
        if self.rect.collidepoint(coords):
            return True
        return False

    def draw(self, screen):

        if self.enabled is False:
            return

        pygame.draw.rect(screen, (121, 85, 61), self.rect, border_radius=20)

        if self.items is not None:
            for i, item in enumerate(self.items):
                item_rect = pygame.Rect(38 + i * (self.scale[0] + 30), 40, *self.scale)
                screen.blit(pygame.transform.scale(item.image_for_ui(), (90, 90)), item_rect)


class Level:

    def __init__(self, level_name, spawn_coords, image, collision_rects, transitions_rects, sprite_group, music=None, foot_step=None):

        self.collision_rects = []
        self.transitions_rects = transitions_rects
        self.name = level_name
        self.list_of_rect = []

        self.sprite_group = sprite_group

        for i in collision_rects:
            self.collision_rects.append(pygame.Rect(i))

        for m in transitions_rects:
            self.list_of_rect.append(pygame.Rect(m))

        self.image = image
        self.rect = self.image.get_rect()
        super().__init__()

        pygame.display.update()
        pygame.display.flip()

        self.spawn_coords = spawn_coords

    def return_sprite(self):
        return self.sprite_group

    def check_transitions(self, player, level):
        for v in self.list_of_rect:
            if player.rect.colliderect(v):
                return True
            return False

    def check_collision(self, player):
        for j in self.collision_rects:
            if player.rect.colliderect(j):
                return True

    def level_name(self):
        return self.name

    def return_image(self):
        return self.image

    def return_spawn(self):
        return self.spawn_coords

all_groups = [

    sprite_groups_manager(street_1, [ply, ]),

    sprite_groups_manager(street_2, [ply, ]),

    sprite_groups_manager(mansion_1, [ply, ]),

    sprite_groups_manager(mansion_2, [ply, ]),

    sprite_groups_manager(mansion_3, [ply, ]),

    sprite_groups_manager(mansion_4, [ply, ]),

    sprite_groups_manager(mansion_5, [ply, ]),

    sprite_groups_manager(mansion_6, [ply, ]),

]
'''ПОМЕНЯТЬ'''
interface = InventoryUI([list_of_items['Candle'], list_of_items['Key']])

current_map = Level('start_street_1', (860, 910),
                    pygame.image.load(os.path.join(assets_path, 'start_home.png')).convert_alpha(),
                    [(0, 0, 2000, 840)], [(1892, 1010, 2000, 1080)], all_groups[0])
spawn_coords = current_map.spawn_coords
x, y = spawn_coords

list_of_levels = {

    'start_street_1': Level('start_street_1', (860, 910),
                            pygame.image.load(os.path.join(assets_path, 'start_home.png')).convert_alpha(),
                            [(0, 0, 2000, 840)], [(1892, 1010, 2000, 1080)], all_groups[0]),

    'start_street_2': Level('start_street_2', (943, 900),
                            pygame.image.load(os.path.join(assets_path, 'start_street.png')).convert_alpha(),
                            [(0, 0, 2000, 724), (3, 884, 839, 543), (2000, 799, 1084, 499)], [(914, 760, 10, 10)],
                            all_groups[1]),

    'mansion_1': Level('mansion_1', (860, 910),
                       pygame.image.load(os.path.join(assets_path, 'mansion_1.png')).convert_alpha(),
                       [(0, 0, 1343, 533)], [(210, 747, 50, 50)], all_groups[2]),

    'mansion_2': Level('mansion_2', (860, 910),
                       pygame.image.load(os.path.join(assets_path, 'mansion_2.png')).convert_alpha(),
                       [(0, 0, 2000, 840)], [(1873, 998, 1999, 1070)], all_groups[3]),

    'mansion_3': Level('mansion_3', (860, 910),
                       pygame.image.load(os.path.join(assets_path, 'mansion_3.png')).convert_alpha(),
                       [(0, 0, 1343, 533)], [], all_groups[4]),

    'mansion_4': Level('mansion_4', (860, 910),
                       pygame.image.load(os.path.join(assets_path, 'mansion_4.png')).convert_alpha(),
                       [(0, 0, 1343, 533)], [], all_groups[5])

}


def handle_click(mouse_pos, current_group):
    for sprite in current_group:  # Здесь street_1 — это группа спрайтов на текущем уровне
        if isinstance(sprite, ClickableSprite):  # Проверяем, что это клик по спрайту
            if sprite.is_clicked(mouse_pos):
                minigame_manager()
                return


def minigame_manager():
    # Код для начала мини-игры
    print("Мини-игра началась!")
    # Допустим, это окно с каким-то действием
    # Пример: pygame.display.set_mode((500, 500)) для нового окна


# def sprite_separator():
#     sheet = Image.open("assets/test_walk.png")


#     count = 0
#
#     for x in range(4):
#         for y in range(4):
#             a = (x + 1) * 128
#             b = (y + 1) * 128
#             icon = sheet.crop((a - 128, b - 128, a, b))
#             icon.save("assets/icons/{}.png".format(count))
#             count += 1
#
# sprite_separator()

def sprite_separator():
    for v in os.listdir('assets/icons'):
        image = Image.open(v)
        new_image = image.resize((300, 300))
        new_image.save("assets/icons/{}.png".format(v))


def intro(screen):
    while True:

        current_path = os.path.dirname(__file__)
        assets_path = os.path.join(current_path, 'assets')

        pygame.mixer.music.load('intro_song.mp3')
        pygame.mixer.music.play()

        x = 50
        y = 500

        player_image = pygame.image.load(os.path.join(assets_path, 'pink_paw.png')).convert_alpha()
        player_imag_ch = pygame.transform.scale(player_image, (125, 125))
        player_imag_ch1 = pygame.transform.rotate(player_imag_ch, -40)
        player_imag_ch2 = pygame.transform.rotate(player_imag_ch, -10)

        for j in range(5):
            screen.blit(player_imag_ch1, (x, y))
            pygame.display.flip()
            x += 210
            y -= 20
            sleep(0.8)
            screen.blit(player_imag_ch2, (x, y))
            pygame.display.flip()
            x += 210
            y -= 20
            sleep(0.8)

        panther_intro = pygame.sprite.Sprite(intro_sprites)
        panther_intro.image = pygame.transform.scale(
            pygame.image.load(os.path.join(assets_path, 'panther_intro.png')).convert_alpha(), (400, 400))
        panther_intro.rect = panther_intro.image.get_rect()

        panther_intro.rect.x = 1700
        panther_intro.rect.y = 690

        for _ in range(20):
            panther_intro.rect.x -= 5
            intro_sprites.update()
            intro_sprites.draw(screen)
            pygame.display.update()
            clock.tick(60)
            screen.fill('BLACK')
        sleep(3)
        for _ in range(40):
            panther_intro.rect.x += 10
            intro_sprites.update()
            intro_sprites.draw(screen)
            pygame.display.update()
            clock.tick(60)
            screen.fill('BLACK')

        logo = pygame.sprite.Sprite(intro_sprites)
        logo.image = pygame.image.load(os.path.join(assets_path, 'panther_logo.png')).convert_alpha()
        logo.rect = logo.image.get_rect()
        logo.rect.x = 250
        logo.rect.y = -10

        sleep(0.5)

        for _ in range(400):
            logo.rect.y += 1
            intro_sprites.update()
            intro_sprites.draw(screen)
            pygame.display.update()
            clock.tick(60)
            screen.fill('BLACK')

        sleep(5)
        intro_sprites.empty()

        sleep(1)

        break
    return


def menu(screen):
    pass


while True:
    event = pygame.event.poll()
    screen = pygame.display.set_mode((0, 0), pygame.FULLSCREEN)
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            exit()

    while True:

        street_1 = current_map.sprite_group
        screen.blit(current_map.return_image(), (0, 0))
        street_1.draw(screen)
        interface.draw(screen)
        pygame.display.flip()

        for event in pygame.event.get():
            if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                ply.standStraight()
                x1, y1 = (pygame.mouse.get_pos
                          ())
                x1 -= 70
                y1 -= 90
                x, y = ply.get_coords()
                if x1 == x and y1 == y:
                    ply.standStraight()
                    street_1.update()
                    street_1.draw(screen)
                    interface.draw(screen)
                    pygame.display.flip()
                elif x1 > x:
                    while x1 > x:
                        x, y = ply.get_coords()
                        if ply.check_borders():
                            ply.rect.x = x - 5
                            break
                        if current_map.check_collision(ply):
                            ply.rect.x = x + 5
                            ply.rect.y = y + 5
                            break
                        if current_map.check_transitions(ply, current_map):
                            level_manager(current_map)
                            ply.rect.x = current_map.spawn_coords[0]
                            ply.rect.y = current_map.spawn_coords[1]
                            ply.standStraight()
                            break
                        if interface.movement_collision((x, y)):
                            break
                        ply.moveRight()
                        screen.blit(current_map.return_image(), (0, 0))
                        street_1.update()
                        street_1.draw(screen)
                        interface.draw(screen)
                        pygame.display.flip()
                        sleep(0.06)
                elif x1 < x:
                    while x1 < x:
                        x, y = ply.get_coords()
                        if ply.check_borders():
                            ply.rect.x = x + 5
                            break
                        if current_map.check_collision(ply):
                            ply.rect.x = x + 5
                            ply.rect.y = y + 5
                            break
                        if current_map.check_transitions(ply, current_map):
                            level_manager(current_map)
                            ply.rect.x = current_map.spawn_coords[0]
                            ply.rect.y = current_map.spawn_coords[1]
                            ply.standStraight()
                            break
                        if interface.movement_collision((x, y)):
                            break
                        ply.moveLeft()
                        screen.blit(current_map.return_image(), (0, 0))
                        street_1.update()
                        street_1.draw(screen)
                        interface.draw(screen)
                        pygame.display.flip()
                        sleep(0.06)
                if y1 > y:
                    while y1 > y:
                        x, y = ply.get_coords()
                        if ply.check_borders():
                            ply.rect.y -= 5
                            break
                        if current_map.check_collision(ply):
                            ply.rect.x = x + 5
                            ply.rect.y = y + 5
                            break
                        if current_map.check_transitions(ply, current_map):
                            level_manager(current_map)
                            ply.rect.x = current_map.spawn_coords[0]
                            ply.rect.y = current_map.spawn_coords[1]
                            ply.standStraight()
                            break
                        if interface.movement_collision((x, y)):
                            break
                        ply.moveForward()
                        screen.blit(current_map.return_image(), (0, 0))
                        street_1.update()
                        street_1.draw(screen)
                        interface.draw(screen)
                        pygame.display.flip()
                        sleep(0.06)
                elif y1 < y:
                    while y1 < y:
                        x, y = ply.get_coords()
                        if ply.check_borders():
                            ply.rect.y = y + 5
                            break
                        if current_map.check_collision(ply):
                            ply.rect.x = x + 5
                            ply.rect.y = y + 5
                            break
                        if current_map.check_transitions(ply, current_map):
                            level_manager(current_map)
                            ply.rect.x = current_map.spawn_coords[0]
                            ply.rect.y = current_map.spawn_coords[1]
                            ply.standStraight()
                            break
                        if interface.movement_collision((x, y)):
                            break
                        ply.moveBack()
                        screen.blit(current_map.return_image(), (0, 0))
                        street_1.update()
                        street_1.draw(screen)
                        interface.draw(screen)
                        pygame.display.flip()
                        sleep(0.06)
            if event.type == pygame.MOUSEBUTTONDOWN and event.button == 3:
                if interface.enabled is True:
                    interface.enabled = False
                elif interface.enabled is False:
                    interface.enabled = True

