from time import sleep

import pygame
import os
from PIL import Image

flag_ = False
flag_2 = False
flag = False
scale = 1.0


music_tracks = {
    "start_street_1": 'sound_for_start.mp3',
    "mansion_1": "sound_for_mansion.mp3",
}


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

        letter = pygame.sprite.Sprite(intro_sprites)
        letter.image = pygame.image.load(os.path.join(assets_path, 'letter.png')).convert_alpha()
        letter.rect = logo.image.get_rect()
        letter.rect.x = 130
        letter.rect.y = 145

        intro_sprites.update()
        intro_sprites.draw(screen)
        pygame.display.update()

        pygame.mixer.music.load(os.path.join(assets_path, 'start_bebe.mp3'))
        pygame.mixer.music.play(loops=1, start=0.1)

        while pygame.mixer.music.get_busy():
            pygame.time.Clock().tick(10)

        screen.fill('BLACK')

        break
    return


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

cur_group = pygame.sprite.Group()
street_2 = pygame.sprite.Group()
mansion_1 = pygame.sprite.Group()
mansion_2 = pygame.sprite.Group()
mansion_3 = pygame.sprite.Group()
mansion_4 = pygame.sprite.Group()
mansion_5 = pygame.sprite.Group()
mansion_6 = pygame.sprite.Group()

intro(screen)

pygame.mixer.init()

object_bring = pygame.mixer.Sound('get_item.mp3')
door_open = pygame.mixer.Sound('open_door.mp3')
melting = pygame.mixer.Sound('vox_burn.mp3')
water_mansion = pygame.mixer.Sound('water_sound.mp3')
crowbar_get = pygame.mixer.Sound('water_sound.mp3')
wooden_door = pygame.mixer.Sound('wooden_door.mp3')
closed_door = pygame.mixer.Sound('closed.mp3')

current_path = os.path.dirname(__file__)
assets_path = os.path.join(current_path, 'assets')


class Player(pygame.sprite.Sprite):
    def __init__(self, x, y, image_folder, scale=(200, 200), foot_step=None):
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

    def check_borders_u(self):
        pass

    def is_equiped(self, item):
        if item in self.inventory:
            return True
        return False

    def remove_item(self, item):
        self.inventory.remove(item)


ply = Player(860, 910, os.path.join(f'{os.curdir}/icons'), (180, 180))


def sprite_groups_manager(group, list_of_sprites):
    for i in list_of_sprites:
        group.add(i)
    return group


def music_manager(level):
    global flag_
    global flag_2
    if level.level_name() == 'start_street_1' and flag_ is False:
        pygame.mixer.music.load(music_tracks[level.level_name()])
        pygame.mixer.music.play(loops=-1, start=0.1)
        flag_ = True
        return
    elif level.level_name() == 'mansion_1' and flag_2 is False:
        pygame.mixer.music.load(music_tracks[level.level_name()])
        pygame.mixer.music.play(loops=-1, start=0.1)
        flag_2 = True
        return


def level_manager(level):
    global flag
    global current_map
    global ply
    if level.level_name() == 'start_street_1':
        current_map = list_of_levels['start_street_2']
        return
    elif level.level_name() == 'start_street_2':
        current_map = list_of_levels['mansion_1']
        return
    elif level.level_name() == 'mansion_1' and ply.is_equiped(list_of_items['Crowbar']):
        current_map = list_of_levels['mansion_2']
        wooden_door.play()
        return
    elif level.level_name() == 'mansion_1' and not ply.is_equiped(list_of_items['Crowbar']):
        closed_door.play()
        return
    elif level.level_name() == 'mansion_2':
        current_map = list_of_levels['mansion_3']
        door_open.play()
        return
    elif level.level_name() == 'mansion_3' and ply.is_equiped(list_of_items['Key']):
        current_map = list_of_levels['mansion_4']
        door_open.play()
        return
    else:
        ply.rect.x -= 5
        ply.rect.y -= 5
    return


class Item(pygame.sprite.Sprite):
    def __init__(self, name, image, coords):
        super().__init__()

        self.name = name
        self.image = pygame.image.load(image)
        self.rect = self.image.get_rect()
        self.x, self.y = coords
        self.rect.x = self.x
        self.rect.y = self.y
        self.name = name

        if self.name == 'Печь':
            self.image = pygame.Surface((50, 50), pygame.SRCALPHA)
            self.image.fill((0, 0, 0, 0))

    def get_name(self):
        return self.name

    def image_for_ui(self):
        return self.image


list_of_items = {

    'Candle': Item('Свечка', os.path.join(assets_path, 'candle.png'), (100, 500)),

    'Key': Item('Ключ', os.path.join(assets_path, 'key.png'), (200, 500)),

    'Vox': Item('Воск', os.path.join(assets_path, 'vox.png'), (1690, 675)),

    'Stove': Item('Печь', os.path.join(assets_path, 'stove.png'), (155, 670)),

    'Water': Item('Печь', os.path.join(assets_path, 'stove.png'), (1395, 955)),

    'Crowbar': Item('Монтировка', os.path.join(assets_path, 'screw.png'), (100, 500)),

    'Lamp': Item('Лампа', os.path.join(assets_path, 'lighter.png'), (1340, 950)),

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

    def __init__(self, level_name, spawn_coords, image, collision_rects, transitions_rects, sprite_group,
                 scale=(180, 180)):

        self.collision_rects = []
        self.transitions_rects = transitions_rects
        self.name = level_name
        self.list_of_rect = []
        self.scale = scale

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

    def return_scale(self):
        return self.scale


all_groups = [

    sprite_groups_manager(cur_group, [ply, ]),

    sprite_groups_manager(street_2, [ply, ]),

    sprite_groups_manager(mansion_1, [ply, list_of_items['Water'], list_of_items['Lamp']]),

    sprite_groups_manager(mansion_2, [ply, ]),

    sprite_groups_manager(mansion_3, [ply, list_of_items['Vox'], list_of_items['Stove']]),

    sprite_groups_manager(mansion_4, [ply, ]),

]
interface = InventoryUI(ply.inventory)

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

    'mansion_1': Level('mansion_1', (860, 870),
                       pygame.image.load(os.path.join(assets_path, 'mansion_1.png')).convert_alpha(),
                       [(0, 0, 1343, 533), (0, 0, 1137, 715)], [(910, 740, 100, 50)], all_groups[2]),

    'mansion_2': Level('mansion_2', (1000, 890),
                       pygame.image.load(os.path.join(assets_path, 'mansion_2.png')).convert_alpha(),
                       [(0, 2004, 500, 3000)], [(910, 360, 235, 412)], all_groups[3], (500, 500)),

    'mansion_3': Level('mansion_3', (660, 950),
                       pygame.image.load(os.path.join(assets_path, 'mansion_3.png')).convert_alpha(),
                       [(0, 0, 1140, 200), (2004, 0, 1140, 200), (650, 267, 200, 535), (1195, 250, 200, 535)],
                       [(935, 720, 50, 50)], all_groups[4], (1000, 1000)),

    'mansion_4': Level('mansion_4', (860, 910),
                       pygame.image.load(os.path.join(assets_path, 'mansion_4.png')).convert_alpha(),
                       [(0, 0, 1343, 533)], [], all_groups[5], (500, 500)),

}


def sprite_separator():
    for v in os.listdir('assets/icons'):
        image = Image.open(v)
        new_image = image.resize((300, 300))
        new_image.save("assets/icons/{}.png".format(v))


def final(screen):

    pygame.mixer.music.load(os.path.join(assets_path, 'my.mp3'))
    pygame.mixer.music.play(loops=1, start=0.1)

    while pygame.mixer.music.get_busy():
        pygame.time.Clock().tick(10)

    sleep(3)

    mesenev = pygame.image.load(os.path.join(assets_path, 'screamer.png'))
    screen.blit(mesenev, (0, 0))
    pygame.display.flip()

    pygame.mixer.music.load(os.path.join(assets_path, 'screamer.mp3'))
    pygame.mixer.music.play(loops=1, start=0.1)

    while pygame.mixer.music.get_busy():
        pygame.time.Clock().tick(10)

    exit()
current_map = list_of_levels['mansion_1']

while True:
    event = pygame.event.poll()
    screen = pygame.display.set_mode((0, 0), pygame.FULLSCREEN)
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            exit()

    while True:

        cur_group = current_map.sprite_group
        music_manager(current_map)
        screen.blit(current_map.return_image(), (0, 0))
        cur_group.draw(screen)
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
                ply.scale = current_map.return_scale()
                if current_map == list_of_levels['mansion_1']:
                    if list_of_items['Water'].rect.collidepoint(pygame.mouse.get_pos()) and not ply.is_equiped(
                            list_of_items['Crowbar']):
                        water_mansion.play()
                        sleep(2)
                        crowbar_get.play()
                        ply.add_item(list_of_items['Crowbar'])
                        break
                if current_map == list_of_levels['mansion_3']:
                    if list_of_items['Vox'].rect.collidepoint(pygame.mouse.get_pos()):
                        object_bring.play()
                        ply.add_item(list_of_items['Vox'])
                        list_of_items['Vox'].kill()
                        break
                    if list_of_items['Stove'].rect.collidepoint(pygame.mouse.get_pos()) and ply.is_equiped(
                            list_of_items['Vox']):
                        ply.remove_item(list_of_items['Vox'])
                        melting.play()
                        ply.add_item(list_of_items['Key'])
                        break
                    pass
                if x1 == x and y1 == y:
                    ply.standStraight()
                    cur_group.update()
                    cur_group.draw(screen)
                    interface.draw(screen)
                    pygame.display.flip()
                elif x1 > x:
                    while x1 > x:
                        x, y = ply.get_coords()
                        if ply.check_borders_u():
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
                            cur_group = current_map.sprite_group
                            break
                        if interface.movement_collision((x, y)):
                            break
                        ply.moveRight()
                        screen.blit(current_map.return_image(), (0, 0))
                        cur_group.update()
                        cur_group.draw(screen)
                        interface.draw(screen)
                        pygame.display.flip()
                        sleep(0.06)
                elif x1 < x:
                    while x1 < x:
                        x, y = ply.get_coords()
                        if ply.check_borders_u():
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
                            cur_group = current_map.sprite_group
                            break
                        if interface.movement_collision((x, y)):
                            break
                        ply.moveLeft()
                        screen.blit(current_map.return_image(), (0, 0))
                        cur_group.update()
                        cur_group.draw(screen)
                        interface.draw(screen)
                        pygame.display.flip()
                        sleep(0.06)
                if y1 > y:
                    while y1 > y:
                        x, y = ply.get_coords()
                        if ply.check_borders_u():
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
                            cur_group = current_map.sprite_group
                            break
                        if interface.movement_collision((x, y)):
                            break
                        ply.moveForward()
                        screen.blit(current_map.return_image(), (0, 0))
                        cur_group.update()
                        cur_group.draw(screen)
                        interface.draw(screen)
                        pygame.display.flip()
                        sleep(0.06)
                elif y1 < y:
                    while y1 < y:
                        x, y = ply.get_coords()
                        if ply.check_borders_u():
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
                            cur_group = current_map.sprite_group
                            break
                        if interface.movement_collision((x, y)):
                            break
                        ply.moveBack()
                        screen.blit(current_map.return_image(), (0, 0))
                        cur_group.update()
                        cur_group.draw(screen)
                        interface.draw(screen)
                        pygame.display.flip()
                        sleep(0.06)
                    if current_map == list_of_levels['mansion_4']:
                        screen.blit(current_map.return_image(), (0, 0))
                        cur_group.update()
                        cur_group.draw(screen)
                        interface.draw(screen)
                        pygame.display.flip()
                        final(screen)
            if event.type == pygame.MOUSEBUTTONDOWN and event.button == 3:
                if interface.enabled is True:
                    interface.enabled = False
                elif interface.enabled is False:
                    interface.enabled = True
