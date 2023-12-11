import pygame


class Game:
    def __init__(self):
        pygame.init()
        pygame.display.set_caption("SpaceShooter")
        # the surface which user see
        self.screen = pygame.display.set_mode()
        # the surface on which the objects are drawn
        self.display = pygame.Surface((320, 240))
        self.clock = pygame.time.Clock()
        self.running = True

        #  x-axis movement in a particular frame
        self.movement = [False, False]
        #  free fall acceleration
        self.acceleration = 0.1
        #  scroll from the origin ([0;0] coordinates)
        self.scroll = [0, 0]

    def run(self):
        while self.running:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.running = False
            pygame.display.flip()
        pygame.quit()


if __name__ == '__main__':
    Game().run()
