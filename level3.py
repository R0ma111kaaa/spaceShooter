import pygame


pygame.init()
screen = pygame.display.set_mode()
fps = 60

BackGround = pygame.transform.scale(pygame.image.load("data/images/background.png"),
                                    (screen.get_width(), screen.get_height()))

boss_health = pygame.transform.scale(pygame.image.load("data/images/entities/boss/Coin1.png"),
                                     (screen.get_width() * 0.05,
                                       screen.get_height() * 0.05))

player_health = pygame.transform.scale(pygame.image.load("data/images/entities/spaceship/player_health.png"),
                                       (screen.get_width() * 0.05,
                                        screen.get_height() * 0.05))

Pacman = pygame.transform.scale(pygame.image.load("data/images/entities/boss/PacMan.png"),
                                (screen.get_width() * 0.2,screen.get_height() * 0.2))


player_group = pygame.sprite.Group()

class Boss(pygame.sprite.Sprite):
    def __init__(self, screen, sheet, colums, rows, x, y):
        super().__init__()
        self.now = 0
        self.last = 0
        self.health = 3
        self.screen = screen
        self.frames = []
        self.cut_sheet(sheet, colums, rows)
        self.cur_frame = 0
        self.image = self.frames[self.cur_frame]
        self.rect = self.rect.move(x, y)
        self.mouvement = self.screen.get_height() * 0.03

    def cut_sheet(self, sheet, columns, rows):
        self.rect = pygame.Rect(0, 0, sheet.get_width() // columns,
                                sheet.get_height() // rows)
        for j in range(rows):
            for i in range(columns):
                frame_location = (int(self.rect.w * i), int(self.rect.h * j))
                self.frames.append(pygame.transform.flip(sheet.subsurface(pygame.Rect(
                    frame_location, self.rect.size)), True, False))
    def update(self):
        self.cur_frame = (self.cur_frame + 1) % len(self.frames)
        self.image = self.frames[self.cur_frame]
        if self.rect.bottom >= self.screen.get_height() - self.screen.get_height() * 0.15 or self.rect.top <= 10:
            self.mouvement *= -1
        self.rect.y += self.mouvement
        if self.cur_frame == 3:
            self.now = pygame.time.get_ticks()
            if self.health == 3 and self.now - self.last >= 300:
                x = Bullet((self.rect.x, self.rect.y), (self.rect.x, self.rect.y + 100),
                           self.screen.get_width(), (255, 255, 255), -1)
                bullet_group_ennemi.add(x)
                self.last = self.now
            elif self.health <= 2 and self.now - self.last >= 250:
                x = Weird_bullet((self.rect.x, self.rect.y), (self.rect.x, self.rect.y + 100),
                                 self.screen.get_width(), (255, 0, 255), -1, -1)
                y = Weird_bullet((self.rect.x, self.rect.y + 10), (self.rect.x, self.rect.y + 110),
                                 self.screen.get_width(), (0, 128, 0), -1, 1)
                bullet_group_ennemi.add(x)
                bullet_group_ennemi.add(y)
                self.last = self.now
            else:
                bullet_group_ennemi.add(Guided((self.rect.x, self.rect.y), (self.rect.x, self.rect.y + 100),
                                               self.screen.get_width(), (255, 255, 255), -1))

        #  bullet_group_ennemi.add(x)



class Spaceship(pygame.sprite.Sprite):
    image = pygame.transform.scale(pygame.image.load("data/images/entities/spaceship/spaceship3.png"),
                                   (screen.get_width() * 0.1,screen.get_height() * 0.1))

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
        self.health = 3

    def update(self, mouvement):
        if mouvement == "up":
            self.rect.y = (self.rect.y - (self.screen.get_height() * 0.03)) % self.screen.get_height()
        elif mouvement == "down":
            self.rect.y = (self.rect.y + (self.screen.get_height()* 0.03)) % self.screen.get_height()
        elif mouvement == "left" and 0 <= self.rect.x + 10:
            self.rect.x -= self.screen.get_width() * 0.02
        elif mouvement == "right" and self.screen.get_width() >= self.rect.x + 10:
            self.rect.x += self.screen.get_width() * 0.02

    def create_bullet(self):
        return Bullet(self.rect.topright, self.rect.bottomright, self.screen.get_width(), (255, 0, 0), 1)


class Bullet(pygame.sprite.Sprite):
    def __init__(self, topright, bottonright, screen_width, bullet, way):
        super().__init__()
        self.image = pygame.Surface((10, 5))
        self.image.fill(bullet)
        self.rect = self.image.get_rect(center=(topright[0], (topright[1] + bottonright[1]) // 2))
        self.screen = screen_width
        self.direction = way

    def update(self):
        if pygame.sprite.collide_mask(self, player):
            player.health -= 1
            self.kill()
        if not pygame.sprite.collide_mask(self, boss):
            self.rect.x += self.direction * (self.screen * 0.02)
        else:
            boss.health -= 1
            self.kill()

        if self.rect.x >= self.screen + 30 or self.rect.x <= -30:
            self.kill()


class Weird_bullet(pygame.sprite.Sprite):
    def __init__(self, topright, bottonright, screen_height, bullet, way, up_down):
        super().__init__()
        self.image = pygame.Surface((10, 5))
        self.image.fill(bullet)
        self.rect = self.image.get_rect(center=(topright[0], (topright[1] + bottonright[1]) // 2))
        self.screen = screen_height
        self.direction = way
        self.stop_x = False
        self.vertical = up_down

    def update(self):
        if pygame.sprite.collide_mask(self, player):
            player.health -= 1
            self.kill()
        if self.stop_x:
            self.rect.y += 20 * self.vertical
        else:
            if self.rect.x <= player.rect.x + 50:
                self.stop_x = True
            self.rect.x += 40 * self.direction

        if self.rect.y >= self.screen or self.rect.y <= 0:
            self.kill()


class Guided(pygame.sprite.Sprite):
    def __init__(self, topright, bottonright, screen_width, bullet, way):
        # НЕОБХОДИМО вызвать конструктор родительского класса Sprite.
        # Это очень важно!!!
        super().__init__()
        self.image = pygame.Surface((10, 5))
        self.image.fill(bullet)
        self.rect = self.image.get_rect(center=(topright[0], (topright[1] + bottonright[1]) // 2))
        self.screen = screen_width
        self.direction = way

    def update(self):
        if pygame.sprite.collide_mask(self, player):
            player.health -= 1
            self.kill()
        d = 0
        if self.rect.y != player.rect.y:
            d = -1 if self.rect.y - player.rect.y >= 0 else 1

        self.rect.y += d * 2
        self.rect.x += self.direction * 2

        if self.rect.y >= self.screen or self.rect.x <= 0:
            self.kill()


boss_group = pygame.sprite.Group()
bullet_group_player = pygame.sprite.Group()
bullet_group_ennemi = pygame.sprite.Group()
player = Spaceship(screen)
last = 0
coldown = 300
boss = Boss(screen, Pacman, 8, 1, int(screen.get_width() - screen.get_width() * 0.1),
            screen.get_height() // 2)

boss_group.add(boss)
player_group.add(player)
clock = pygame.time.Clock()
running = True

while running:
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
            now = pygame.time.get_ticks()
            if len(bullet_group_player) <= 3 and now - last >= coldown:
                bullet_group_player.add(player.create_bullet())
                last = now

    screen.blit(BackGround, (0, 0))
    for i in range(1, boss.health + 1):
        screen.blit(boss_health, (screen.get_width() - (i * screen.get_width() * 0.06), 10))
    for i in range(player.health):
        screen.blit(player_health, ((i * screen.get_width() * 0.06), 10))

    bullet_group_player.draw(screen)
    bullet_group_ennemi.draw(screen)
    player_group.draw(screen)
    boss_group.draw(screen)
    bullet_group_player.update()
    bullet_group_ennemi.update()
    player_group.update(mouvement)
    boss_group.update()

    pygame.display.flip()
    if boss.health == 0 or player.health == 0:
        running = False
pygame.quit()
