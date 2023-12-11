import pygame


class Game:
    def __init__(self):
        pygame.init()
        self.screen = pygame.display.set_mode()
        self.display = pygame.Surface((320, 240))
        self.running = True

    def run(self):
        while self.running:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.running = False
            pygame.display.flip()
        pygame.quit()


if __name__ == '__main__':
    Game().run()
