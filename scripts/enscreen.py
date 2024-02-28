import pygame

class Endscreen(pygame.sprite.Sprite):
    image1 = pygame.image.load("data/Design_menu/youwin.png")
    image2 = pygame.image.load("data/Design_menu/youlose.png")

    def __init__(self, screen, state):
        super().__init__()
        if state:
            self.image = pygame.transform.scale(Endscreen.image1, screen.get_size())
        else:
            self.image = pygame.transform.scale(Endscreen.image2, screen.get_size())
        self.rect = self.image.get_rect()
        self.rect.x = - screen.get_width()
        self.rect.y = 0
    def update(self):
        if self.rect.x <= -3:
            self.rect = self.rect.move(40, 0)
