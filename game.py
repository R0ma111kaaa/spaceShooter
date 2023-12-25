import pygame

from scripts.entities import Player
from scripts.tilemap import Tilemap
from scripts.utils import load_image, load_images, Animation


class Game:
    def __init__(self):
        pygame.init()
        pygame.display.set_caption("SpaceShooter")
        # the surface which user see
        self.screen = pygame.display.set_mode()
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
            'empty': load_image('empty.png'),
            'decor': load_images('tiles/decor'),
            'grass': load_images('tiles/grass'),
            'large_decor': load_images('tiles/large_decor'),
            'stone': load_images('tiles/stone'),
            'background': load_image('background.png', png=False),
            'player': load_image('empty.png'),
            'player/idle': Animation(load_images('entities/player/idle'), img_dur=6),
            'player/run': Animation(load_images('entities/player/run'), img_dur=4),
            'player/jump': Animation(load_images('entities/player/jump')),
        }

        self.tilemap = Tilemap(self)
        self.tilemap.load('map.json')

        self.player = Player(self, (self.tilemap.player_pos[0] * self.tilemap.tile_size,
                                    self.tilemap.player_pos[1] * self.tilemap.tile_size), (8, 15))

    def run(self):
        while self.running:
            self.scroll[0] += (self.player.rect().centerx - self.display.get_width() / 2 - self.scroll[0]) / 30
            self.scroll[1] += (self.player.rect().centery - self.display.get_height() / 2 - self.scroll[1]) / 30
            render_scroll = (int(self.scroll[0]), int(self.scroll[1]))

            self.display.blit(pygame.transform.scale(self.assets['background'], self.display.get_size()), (0, 0))

            self.tilemap.render(self.display, render_scroll)

            self.player.update(self.tilemap, (self.movement[1] - self.movement[0], 0))
            self.player.render(self.display, render_scroll)

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
                elif event.type == pygame.KEYUP:
                    if event.key == pygame.K_a:
                        self.movement[0] = False
                    elif event.key == pygame.K_d:
                        self.movement[1] = False
            if self.player.win_cod == 1:
               # print("yes")
                self.running = False


            self.screen.blit(pygame.transform.scale(self.display, self.screen.get_size()), (0, 0))
            pygame.display.update()
            self.clock.tick(self.fps)


if __name__ == '__main__':
    Game().run()
