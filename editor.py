import sys
import pygame

from scripts.tilemap import Tilemap
from scripts.utils import load_images


class Editor:
    def __init__(self):
        pygame.init()
        pygame.display.set_caption("TileEditor")
        # the surface which user see
        self.screen = pygame.display.set_mode()
        # the surface on which the objects are drawn
        self.display = pygame.Surface((960, 540))

        # ratio between the player's screen and object render screen
        self.ratio_x = self.screen.get_size()[0] / self.display.get_size()[0]
        self.ratio_y = self.screen.get_size()[1] / self.display.get_size()[1]

        self.running = True

        # movement in a particular frame
        #                left   right   top    down
        self.movement = [False, False, False, False]
        #  scroll from the origin ([0;0] coordinates)
        self.scroll = [0, 0]

        self.assets = {
           # 'player': load_images('tiles/player'),
            'grass': load_images('tiles/grass'),
            'stone': load_images('tiles/stone'),
            'decor': load_images('tiles/decor'),
            'large_decor': load_images('tiles/large_decor'),
            'spawners': load_images('tiles/spawners'),
        }
        self.tiles = list(self.assets)
        self.tile_group = 0
        self.tile_variant = 0
        self.shift = False
        self.ongrid = True
        self.clicking = False
        self.right_clicking = False

        self.tilemap = Tilemap(self)
        try:
            self.tilemap.load('map2.json')
        except FileNotFoundError:
            pass

    def run(self):
        while self.running:
            self.scroll[0] += (self.movement[1] - self.movement[0]) * self.ratio_x
            self.scroll[1] += (self.movement[3] - self.movement[2]) * self.ratio_y
            render_scroll = (int(self.scroll[0]), int(self.scroll[1]))

            self.display.fill('black')
            self.tilemap.render(self.display, render_scroll, player_pos=True)

            # current tile at mouse position
            current_img = self.assets[self.tiles[self.tile_group]][self.tile_variant].copy()

            mpos = pygame.mouse.get_pos()
            mpos = (mpos[0] / self.ratio_x, mpos[1] / self.ratio_y)
            tile_pos = (int((mpos[0] + self.scroll[0]) / self.tilemap.tile_size),
                        int((mpos[1] + self.scroll[1]) / self.tilemap.tile_size))

            if self.ongrid:
                self.display.blit(current_img, (tile_pos[0] * self.tilemap.tile_size - self.scroll[0],
                                                tile_pos[1] * self.tilemap.tile_size - self.scroll[1]))
            else:
                self.display.blit(current_img, mpos)

            if self.clicking and self.ongrid:
                if self.tiles[self.tile_group] == 'player':
                    self.tilemap.player_pos = tile_pos
                    self.tilemap.tilemap.pop(str(tile_pos[0]) + ';' + str(tile_pos[1]), None)
                elif tile_pos != self.tilemap.player_pos:
                    self.tilemap.tilemap[str(tile_pos[0]) + ';' + str(tile_pos[1])] = {
                        'type': self.tiles[self.tile_group],
                        'variant': self.tile_variant,
                        'pos': tile_pos
                    }
            if self.right_clicking:
                self.tilemap.tilemap.pop(str(tile_pos[0]) + ';' + str(tile_pos[1]), None)
                for tile in self.tilemap.offgrid_tiles.copy():
                    img = self.assets[tile['type']][tile['variant']]
                    tile_r = pygame.Rect(tile['pos'][0] - self.scroll[0], tile['pos'][1] - self.scroll[1],
                                         img.get_width(), img.get_height())
                    if tile_r.collidepoint(mpos):
                        self.tilemap.offgrid_tiles.remove(tile)

            # current tile in top left corner
            top_left_img = current_img.copy()
            top_left_img.set_alpha(170)
            self.display.blit(current_img, (10, 10))

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.running = False
                elif event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_a:
                        self.movement[0] = True
                    elif event.key == pygame.K_d:
                        self.movement[1] = True
                    elif event.key == pygame.K_w:
                        self.movement[2] = True
                    elif event.key == pygame.K_s:
                        self.movement[3] = True
                    elif event.key == pygame.K_g:
                        self.ongrid = not self.ongrid
                    elif event.key == pygame.K_LSHIFT:
                        self.shift = True
                    elif event.key == pygame.K_o:
                        self.tilemap.save('map2.json')
                    elif event.key == pygame.K_t:
                        self.tilemap.autotile()
                        print(f'tilepos: {tile_pos[0] * self.tilemap.tile_size, tile_pos[1] * self.tilemap.tile_size}')
                        print('mpos: ' + str(mpos[0] + self.scroll[0]) + ', ' + str(mpos[1] + self.scroll[1]))
                elif event.type == pygame.KEYUP:
                    if event.key == pygame.K_a:
                        self.movement[0] = False
                    elif event.key == pygame.K_d:
                        self.movement[1] = False
                    elif event.key == pygame.K_w:
                        self.movement[2] = False
                    elif event.key == pygame.K_s:
                        self.movement[3] = False
                    elif event.key == pygame.K_LSHIFT:
                        self.shift = False
                elif event.type == pygame.MOUSEBUTTONDOWN:
                    if event.button == 1:
                        self.clicking = True
                        if not self.ongrid:
                            self.tilemap.offgrid_tiles.append(
                                {'type': self.tiles[self.tile_group],
                                 'variant': self.tile_variant,
                                 'pos': (mpos[0] + self.scroll[0], mpos[1] + self.scroll[1])})
                    elif event.button == 3:
                        self.right_clicking = True
                    elif event.button == 4:
                        if self.shift:
                            self.tile_variant = (self.tile_variant + 1) \
                                                % len(self.assets[self.tiles[self.tile_group]])
                        else:
                            self.tile_group = (self.tile_group + 1) % len(self.tiles)
                            self.tile_variant = 0
                    elif event.button == 5:
                        if self.shift:
                            self.tile_variant = (self.tile_variant - 1) \
                                                % len(self.assets[self.tiles[self.tile_group]])
                        else:
                            self.tile_group = (self.tile_group - 1) % len(self.tiles)
                            self.tile_variant = 0
                elif event.type == pygame.MOUSEBUTTONUP:
                    if event.button == 1:
                        self.clicking = False
                    elif event.button == 3:
                        self.right_clicking = False

            self.screen.blit(pygame.transform.scale(self.display, self.screen.get_size()), (0, 0))
            pygame.display.update()
        pygame.quit()


if __name__ == '__main__':
    Editor().run()
