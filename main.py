from time import sleep

import pygame
import os
from PIL import Image


class Player(pygame.sprite.Sprite):
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



class Level:
    pass


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
        logo.rect.x = 270
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

        house_background = pygame.sprite.Sprite(intro_sprites)
        house_background.image = pygame.image.load(os.path.join(assets_path, 'intro_house.png')).convert_alpha()
        house_background.rect = house_background.image.get_rect()
        house_background.rect.x = 0
        house_background.rect.y = 0

        cat = Player(300, 300, f'{os.curdir}/icons')
        intro_sprites.add(cat)

        while True:
            while cat.get_coords()[1] != 600:
                cat.moveForward()
                intro_sprites.update()
                intro_sprites.draw(screen)
                pygame.display.flip()
                clock.tick(5)
                screen.fill('BLACK')


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
    menu_sprites = pygame.sprite.Group()
    intro(screen)


def game():
    pass


def menu():
    pass


while True:
    screen = pygame.display.set_mode((0, 0), pygame.FULLSCREEN)
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            exit()

    while True:
        pass