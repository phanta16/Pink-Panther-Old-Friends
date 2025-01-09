from time import sleep

import pygame
import os


class Sprites(pygame.sprite.Sprite):
    def __init__(self, name, height, width):
        super().__init__()
        self.image = pygame.image.load(os.path.join(os.getcwd(), name)).convert_alpha()
        self.image = pygame.transform.scale(self.image, (height, width))
        self.rect = self.image.get_rect()
        WIDTH, HEIGHT = self.image.get_size()
        self.rect.center = (WIDTH / 2, HEIGHT / 2)

    def moveRight(self, pixels):
        self.rect.x += pixels

    def moveLeft(self, pixels):
        self.rect.x -= pixels

    def moveForward(self, pixels):
        self.rect.y += pixels

    def moveBack(self, pixels):
        self.rect.y -= pixels

class Player(Sprites):
    pass


class Item(Sprites):
    pass


if __name__ == '__main__':
    pygame.init()
    pygame.display.set_caption('Pink Panther: Old Friend')
    os.chdir(f'{os.getcwd()}\\assets')
    screen = pygame.display.set_mode((0, 0), pygame.FULLSCREEN)
    screen.fill('black')
    pygame.display.update()
    pygame.mixer.init()
    clock = pygame.time.Clock()
    all_sprites = pygame.sprite.Group()


def game():
    pass


def options():
    pass


def menu():
    pass


def intro(screen):
    global player_imag_ch2, player_imag_ch1
    while True:
        x = 50
        y = 500

        current_path = os.path.dirname(__file__)
        image_path = os.path.join(current_path, 'assets')
        player_image = pygame.image.load(os.path.join(image_path, 'pink_paw.png')).convert_alpha()
        player_imag_ch = pygame.transform.scale(player_image, (125, 125))
        player_imag_ch1 = pygame.transform.rotate(player_imag_ch, -40)
        player_imag_ch2 = pygame.transform.rotate(player_imag_ch, -10)

        for j in range(5):
            screen.blit(player_imag_ch1, (x, y))
            pygame.display.flip()
            x += 210
            y -= 20
            sleep(0.5)
            screen.blit(player_imag_ch2, (x, y))
            pygame.display.flip()
            x += 210
            y -= 20
            sleep(0.5)

        panther_intro = Sprites('panther_intro.png', 200, 200)
        panther_intro.rect.x = 1900
        panther_intro.rect.y = 910

        for _ in range(10):
            all_sprites.add(panther_intro)
            panther_intro.moveLeft(10)
            all_sprites.update()
            all_sprites.draw(screen)
            pygame.display.update()
            clock.tick(60)
        break
    return


while True:
    screen = pygame.display.set_mode((0, 0), pygame.FULLSCREEN)
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            exit()
    intro(screen)
    sleep(5)
    exit()
