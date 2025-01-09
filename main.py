from time import sleep

import pygame
import os

class Sprites(pygame.sprite.Sprite):
    pass

class Player(Sprites):
    pass


class Item(Sprites):
    pass

if __name__ == '__main__':
    pygame.init()
    pygame.display.set_caption('Pink Panther: Old Friend')
    current_dir = os.getcwd()
    os.chdir(f'{current_dir}\\assets')
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
    while True:
        visible_area = screen.get_size()
        x = 50
        y = 500

        for image in os.curdir:
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


while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            exit()
    intro(screen)
    menu()
    '''https://lms.yandex.ru/courses/1180/groups/23822/lessons/6992/materials/20596'''
    '''СДЕЛАТЬ НОВЫЙ РЕПОЗИТОРИЙ И ДИРЕКТОРИЮ!'''
