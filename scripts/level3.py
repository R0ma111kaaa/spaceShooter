import pygame
import random
import os
import sys


pygame.init()
size = fat, up = 500, 500
screen = pygame.display.set_mode(size)


def load_image(name, colorkey=None):
    fullname = os.path.join('data','images','entities', 'spaceship', name)
    # если файл не существует, то выходим
    if not os.path.isfile(fullname):
        print(f"Файл с изображением '{fullname}' не найден")
        sys.exit()
    image = pygame.image.load(fullname)
    if colorkey is not None:
        image = image.convert()
        if colorkey == -1:
            colorkey = image.get_at((0, 0))
        image.set_colorkey(colorkey)
    else:
        image = image.convert_alpha()
    return image

all_sprites = pygame.sprite.Group()
hero = pygame.sprite.Sprite(all_sprites)

class Spaceship(pygame.sprite.Sprite):
    image = pygame.image.load("data/images/entities/spaceship/spaceship.png")
    #load_image("spaceship.png")
    def __init__(self, *group):
        # НЕОБХОДИМО вызвать конструктор родительского класса Sprite.
        # Это очень важно!!!
        super().__init__(*group)
        self.image = Spaceship.image
        self.rect = self.image.get_rect()
        self.health = 3

    def update(self):
        pass
class Boss(pygame.sprite.Sprite):

dt = 10
clock = pygame.time.Clock()
running = True
while running:
    clock.tick(30)
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        key = pygame.key.get_pressed()
        if key[pygame.K_UP] and hero.rect.top + 10 > 5:
            hero.rect.top -= dt
        elif key[pygame.K_DOWN] and hero.rect.bottom + 10 <= 501:
            hero.rect.top += dt
        elif key[pygame.K_LEFT] and hero.rect.left + 10 > 10:
            hero.rect.left -= dt
        elif key[pygame.K_RIGHT] and hero.rect.right + 10 <= 510:
            hero.rect.left += dt

    screen.fill(pygame.Color("white"))
    all_sprites.draw(screen)
    pygame.display.flip()
pygame.quit()