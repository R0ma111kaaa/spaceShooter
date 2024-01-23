import pygame
import random
import os
import sys

BackGround = pygame.image.load("data/images/background.png")
pygame.init()
size = fat, up = 500, 500
screen = pygame.display.set_mode(size)
fps = 60


# extra = image.get_bounding_rect()
# trimmed_surface = pygame.Surface(extra.size)
def load_image(name, colorkey=None):
    fullname = os.path.join('data/images/entities/spaceship', name)
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


player_group = pygame.sprite.Group()


class Boss(pygame.sprite.Sprite):
    boss_image = pygame.transform.scale(pygame.image.load("data/images/entities/boss/packman1.png"),
                                        (int(fat * 0.3), int(up * 0.3)))

    def __init__(self, screen):
        super().__init__()
        self.screen = screen
        self.image = pygame.transform.flip(Boss.boss_image, True, False)
        self.rect = self.image.get_rect()
        self.mask = pygame.mask.from_surface(self.image)
        self.rect.x = int(screen.get_width() * 0.7)
        self.rect.y = screen.get_height() // 2
        self.mouvement = 2

    def update(self):
        if self.rect.bottom == self.screen.get_height() or self.rect.top == 0:
            self.mouvement *= -1
        self.rect.y += self.mouvement


class Spaceship(pygame.sprite.Sprite):
    image = pygame.transform.scale(load_image("spaceship3.png"), (int(fat * 0.2), int(up * 0.2)))

    def __init__(self, screen):
        # НЕОБХОДИМО вызвать конструктор родительского класса Sprite.
        # Это очень важно!!!
        super().__init__()
        self.image = Spaceship.image
        # self.mask = pygame.mask.from_surface(self.image)
        self.rect = self.image.get_rect()
        self.rect.x = 10
        self.rect.y = screen.get_height() // 2
        self.screen = screen

    def update(self, mouvement):
        if mouvement == "up":
            self.rect.y = (self.rect.y - 10) % self.screen.get_height()
        elif mouvement == "down":
            self.rect.y = (self.rect.y + 10) % self.screen.get_height()
        elif mouvement == "left" and 0 <= self.rect.x + 10:
            self.rect.x -= 10
        elif mouvement == "right" and self.screen.get_width() >= self.rect.x + 10:
            self.rect.x += 10

    def create_bullet(self):
        return Bullet(self.rect.topright, self.rect.bottomright, self.screen.get_width())


class Bullet(pygame.sprite.Sprite):
    def __init__(self, topright, bottonright, screen_width):
        # НЕОБХОДИМО вызвать конструктор родительского класса Sprite.
        # Это очень важно!!!
        super().__init__()
        self.image = pygame.Surface((10, 5))
        self.image.fill((255, 0, 0))
        self.rect = self.image.get_rect(center=(topright[0], (topright[1] + bottonright[1]) // 2))
        self.screen = screen_width

    def update(self):
        if not pygame.sprite.collide_mask(self, boss):
            self.rect.x += 15
        else:
            self.kill()

        if self.rect.x >= self.screen + 100:
            self.kill()


boss_group = pygame.sprite.Group()
bullet_group = pygame.sprite.Group()
player = Spaceship(screen)
boss = Boss(screen)
boss_group.add(boss)
player_group.add(player)
pygame.transform.scale(BackGround, (screen.get_width(), screen.get_height()))
dt = 10
clock = pygame.time.Clock()
running = True
while running:
    clock.tick(fps)
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        mouvement = 0
        key = pygame.key.get_pressed()
        if key[pygame.K_UP]:
            mouvement = "up"
        elif key[pygame.K_DOWN]:
            mouvement = "down"
        elif key[pygame.K_LEFT]:
            mouvement = "left"
        elif key[pygame.K_RIGHT]:
            mouvement = "right"
        if key[pygame.K_SPACE]:
            bullet_group.add(player.create_bullet())

    screen.blit(BackGround, (0, 0))
    bullet_group.draw(screen)
    player_group.draw(screen)
    boss_group.draw(screen)
    bullet_group.update()
    player_group.update(mouvement)
    boss_group.update()
    pygame.display.flip()
pygame.quit()
