import sys
import random
import math

import pygame

from scripts.entities import Player, Enemy
from scripts.tilemap import Tilemap
from scripts.utils import load_image, load_images, Animation
from scripts.particle import Particle
from scripts.spark import Spark


class Game:
    def __init__(self, level_num=1):
        pygame.init()
        pygame.display.set_caption("SpaceShooter")
        # the surface which user see
        self.screen = pygame.display.set_mode()
        if level_num == 1:
            self.name_json = "map.json"
        elif level_num == 2:
            self.name_json = "map_2.json"
        elif level_num == 3:
            self.name_json = "map_3.json"
        # the surface on which the objects are drawn
        self.display = pygame.Surface((480, 270))
        self.clock = pygame.time.Clock()
        self.running = True

        #  x-axis movement in a particular frame
        self.movement = [False, False]
        #  free fall acceleration
        self.acceleration = 0.1
        #  scroll from the origin ([0;0] coordinates)
        self.scroll = [0, 0]

        self.fps = 60

        self.assets = {
            'decor': load_images('tiles/decor'),
            'grass': load_images('tiles/grass'),
            'large_decor': load_images('tiles/large_decor'),
            'stone': load_images('tiles/stone'),
            'background': load_image('background.png', png=False),
            'player': load_image('empty.png'),
            'player/idle': Animation(load_images('entities/player/idle'), img_dur=6),
            'player/run': Animation(load_images('entities/player/run'), img_dur=4),
            'player/jump': Animation(load_images('entities/player/jump')),
            'player/slide': Animation(load_images('entities/player/slide')),
            'player/wall_slide': Animation(load_images('entities/player/wall_slide')),

            'enemy/idle': Animation(load_images("entities/enemy/idle"), img_dur=6),
            'enemy/run': Animation(load_images("entities/enemy/run"), img_dur=4),
            'projectile': load_image('projectile.png'),
            'gun': load_image('gun.png'),
            'particle/particle': Animation(load_images('particles/particle'), img_dur=6, loop=False),
        }
        self.player = Player(self, ((50, 50)), (8, 15))
        self.tilemap = Tilemap(self)
        self.load_level()

    def load_level(self):
        self.tilemap.load(self.name_json)

        self.enemies = []
        for spawner in self.tilemap.extract([('spawners', 0), ('spawners', 1)]):
            if spawner['variant'] == 0:
                self.player.pos = spawner['pos']
            else:
                self.enemies.append(Enemy(self, spawner['pos'], (8, 15)))

        self.projectiles = []
        self.death = 0
        self.sparks = []
        self.particles = []

    def run(self):
        while self.running:
            self.display.blit(pygame.transform.scale(self.assets['background'], self.display.get_size()), (0, 0))

            if self.death:
                self.death += 1
                if self.death > 40:
                    sys.exit()

            self.scroll[0] += (self.player.rect().centerx - self.display.get_width() / 2 - self.scroll[0]) / 30
            self.scroll[1] += (self.player.rect().centery - self.display.get_height() / 2 - self.scroll[1]) / 30
            render_scroll = (int(self.scroll[0]), int(self.scroll[1]))

            self.tilemap.render(self.display, offset=render_scroll)

            for enemy in self.enemies.copy():
                kill = enemy.update(self.tilemap, (0, 0))
                enemy.render(self.display, offset=render_scroll)
                if kill:
                    self.enemies.remove(enemy)

            if not self.death:
                self.player.update(self.tilemap, (self.movement[1] - self.movement[0], 0))
                self.player.render(self.display, offset=render_scroll)

            for projectile in self.projectiles.copy():
                projectile[0][0] += projectile[1]
                projectile[2] += 1
                img = self.assets['projectile']
                self.display.blit(img, (projectile[0][0] - img.get_width() / 2 - render_scroll[0],
                                            projectile[0][1] - img.get_height() / 2 - render_scroll[1]))
                if self.tilemap.solid_check(projectile[0]):
                    self.projectiles.remove(projectile)
                    for i in range(4):
                        self.sparks.append(
                            Spark(projectile[0], random.random() - 0.5 + (math.pi if projectile[1] > 0 else 0),
                                      2 + random.random()))
                elif projectile[2] > 360:
                        self.projectiles.remove(projectile)
                elif abs(self.player.dashing) < 50:
                    if self.player.rect().collidepoint(projectile[0]):
                        self.projectiles.remove(projectile)
                        self.death += 1
                        for i in range(30):
                            angle = random.random() * math.pi * 2
                            speed = random.random() * 5
                            self.sparks.append(Spark(self.player.rect().center, angle, 2 + random.random()))
                            self.particles.append(Particle(self, 'particle', self.player.rect().center,
                                                               velocity=[math.cos(angle + math.pi) * speed * 0.5,
                                                                         math.sin(angle + math.pi) * speed * 0.5],
                                                               frame=random.randint(0, 7)))

            for spark in self.sparks.copy():
                kill = spark.update()
                spark.render(self.display, offset=render_scroll)
                if kill:
                    self.sparks.remove(spark)

            for particle in self.particles.copy():
                kill = particle.update()
                particle.render(self.display, offset=render_scroll)
                if kill:
                    self.particles.remove(particle)

            # self.player.update(self.tilemap, (self.movement[1] - self.movement[0], 0))
            # self.player.render(self.display, render_scroll)

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.running = False
                elif event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_a:
                        self.movement[0] = True
                    elif event.key == pygame.K_d:
                        self.movement[1] = True
                    elif event.key == pygame.K_w:
                        self.player.jump()
                    elif event.key == pygame.K_SPACE:
                        self.player.dash()
                elif event.type == pygame.KEYUP:
                    if event.key == pygame.K_a:
                        self.movement[0] = False
                    elif event.key == pygame.K_d:
                        self.movement[1] = False

            self.screen.blit(pygame.transform.scale(self.display, self.screen.get_size()), (0, 0))
            pygame.display.update()
            self.clock.tick(self.fps)
        pygame.quit()


if __name__ == '__main__':
    Game().run()
