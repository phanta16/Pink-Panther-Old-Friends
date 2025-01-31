from time import sleep

import pygame
import os
from PIL import Image

flag = False

if __name__ == '__main__':
    pygame.init()
    pygame.display.set_caption('Pink Panther: Old Friend')
    os.chdir(f'{os.getcwd()}\\assets')
    screen = pygame.display.set_mode((0, 0), pygame.FULLSCREEN)
    screen.fill('black')
    pygame.display.update()
    pygame.mixer.init()
    clock = pygame.time.Clock()
    intro_sprites = pygame.sprite.Group()
    first_scene_group = pygame.sprite.Group()
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
    def __init__(self, x, y, image_folder, frame_rate=10):
        super().__init__()

        self.frames = []
        for filename in sorted(os.listdir(image_folder)):
            if filename.endswith('.png'):
                frame = pygame.image.load(os.path.join(image_folder, filename))

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

    def moveForward(self):
        self.frames = [pygame.image.load(os.path.join(f'{os.curdir}/icons', file)) for file in
                       os.listdir(f'{os.curdir}/icons') if 'forward' in file]
        self.rect.y += 5

    def moveBack(self):
        self.frames = [pygame.image.load(os.path.join(f'{os.curdir}/icons', file)) for file in
                       os.listdir(f'{os.curdir}/icons') if 'back' in file]
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


def level_manager(level=None):
    global flag
    if flag is False:
        flag = True
        return list_of_levels['start_street_1']
    if level.level_name() == 'start_street_1':
        return list_of_levels['start_street_2']


class Level(pygame.sprite.Sprite):
    def __init__(self, level_name, spawn_coords, image, collision_rects, transitions_rects, sprite_group):

        self.collision_rects = []
        self.transitions_rects = []
        self.name = level_name

        for i in collision_rects:
            self.collision_rects.append(pygame.Rect(i))

        for m in transitions_rects:
            self.transitions_rects.append(pygame.Rect(m))

        pygame.display.update()
        pygame.display.flip()

        self.spawn_coords = spawn_coords

        self.image = image

        self.rect = self.image.get_rect()
        super().__init__()

    def check_transitions(self, player, level):
        for v in self.transitions_rects:
            if player.rect.colliderect(v):
                # return level_manager(self)
                print('f')
            else:
                return False

    def check_collision(self, player):
        for j in self.collision_rects:
            if player.rect.colliderect(j):
                return True

    def level_name(self):
        return self.name

    def return_spawn(self):
        return self.spawn_coords


list_of_levels = {

    'start_street_1': Level('start_street_1', (860, 910),
                            pygame.image.load(os.path.join(assets_path, 'start_home.png')).convert_alpha(),
                            [(0, 0, 2000, 840)], [(1873, 998, 1999, 1070)], 'change'),

    'start_street_2': Level('start_street_2', (860, 910),
                            pygame.image.load(os.path.join(assets_path, 'start_street.png')).convert_alpha(),
                            [(0, 0, 1343, 533)], [(601, 524, 640, 539)], 'change')

}


class Item(pygame.sprite.Sprite):
    pass


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


current_map = level_manager()
spawn_coords = current_map.spawn_coords
x, y = spawn_coords
ply = Player(x, y, os.path.join(f'{os.curdir}/icons'))
current_map = list_of_levels['start_street_1']
first_scene_group.add(current_map)
first_scene_group.add(ply)


while True:
    screen = pygame.display.set_mode((0, 0), pygame.FULLSCREEN)
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            exit()

    while True:

        first_scene_group.draw(screen)
        pygame.display.flip()

        for event in pygame.event.get():
            if event.type == pygame.MOUSEBUTTONDOWN:
                ply.standStraight()
                x1, y1 = pygame.mouse.get_pos()
                x1 -= 70
                y1 -= 90
                x, y = ply.get_coords()
                if x1 == x and y1 == y:
                    ply.standStraight()
                    first_scene_group.update()
                    first_scene_group.draw(screen)
                    pygame.display.flip()
                    break
                elif x1 > x:
                    while x1 > x:
                        x, y = ply.get_coords()
                        if current_map.check_collision(ply):
                            ply.rect.x = x + 5
                            ply.rect.y = y + 5
                            break
                        if current_map.check_transitions(ply, current_map):
                            current_map = current_map.check_transitions(ply, current_map)
                            break
                        ply.moveRight()
                        first_scene_group.update()
                        first_scene_group.draw(screen)
                        pygame.display.flip()
                        sleep(0.06)
                elif x1 < x:
                    while x1 < x:
                        x, y = ply.get_coords()
                        if current_map.check_collision(ply):
                            ply.rect.x = x + 5
                            ply.rect.y = y + 5
                            break
                        if current_map.check_transitions(ply, current_map):
                            current_map = current_map.check_transitions(ply, current_map)
                            break
                        ply.moveLeft()
                        first_scene_group.update()
                        first_scene_group.draw(screen)
                        pygame.display.flip()
                        sleep(0.06)
                if y1 > y:
                    while y1 > y:
                        x, y = ply.get_coords()
                        if current_map.check_collision(ply):
                            ply.rect.x = x + 5
                            ply.rect.y = y + 5
                            break
                        if current_map.check_transitions(ply, current_map):
                            current_map = current_map.check_transitions(ply, current_map)
                            break
                        ply.moveForward()
                        first_scene_group.update()
                        first_scene_group.draw(screen)
                        pygame.display.flip()
                        sleep(0.06)
                elif y1 < y:
                    while y1 < y:
                        x, y = ply.get_coords()
                        if current_map.check_collision(ply):
                            ply.rect.x = x + 5
                            ply.rect.y = y + 5
                            break
                        if current_map.check_transitions(ply, current_map):
                            current_map = current_map.check_transitions(ply, current_map)
                            break
                        ply.moveBack()
                        first_scene_group.update()
                        first_scene_group.draw(screen)
                        pygame.display.flip()
                        sleep(0.06)
