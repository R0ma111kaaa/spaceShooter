import pygame
import sys
from game import Game

BG = pygame.image.load("data/Design_menu/spacebackground.png")
BG = pygame.transform.scale(BG, (800, 800))





pygame.init()
pygame.display.set_caption("Main Menu")
screen = pygame.display.set_mode((800, 800))
pygame.display.set_caption("Button!")
main_font = pygame.font.Font("data/Design_menu/font.ttf", 45)


class Button:
    def __init__(self, image, x_pos, y_pos, text_input, main_font):
        self.image = image
        self.x_pos = x_pos
        self.y_pos = y_pos
        self.rect = self.image.get_rect(center=(self.x_pos, self.y_pos))
        self.text_input = text_input
        self.text = main_font.render(self.text_input, True, "white")
        self.text_rect = self.text.get_rect(center=(self.x_pos, self.y_pos))

    def update(self):
        screen.blit(self.image, self.rect)
        screen.blit(self.text, self.text_rect)

    def checkForInput(self, position):
        if position[0] in range(self.rect.left, self.rect.right) and position[1] in range(self.rect.top,
                                                                                          self.rect.bottom):
            return True

    def changeColor(self, position):
        if position[0] in range(self.rect.left, self.rect.right) and position[1] in range(self.rect.top,
                                                                                          self.rect.bottom):
            self.text = main_font.render(self.text_input, True, "green")
        else:
            self.text = main_font.render(self.text_input, True, "white")


button_surface = pygame.image.load("data/Design_menu/button2.png")
#  button_surface = load_image("button.png")
button_surface = pygame.transform.scale(button_surface, (500, 200))

start = Button(button_surface, 400, 250, "Start Game", main_font)
options = Button(button_surface, 400, 450, "Options", main_font)
quit = Button(button_surface, 400, 650, "Exit", main_font)
button_group = [start, options, quit]

game_start = False
exit = True
while exit:
    screen.blit(BG, (0, 0))
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()
        if event.type == pygame.MOUSEBUTTONDOWN:
            game_start = start.checkForInput(pygame.mouse.get_pos())
            exit = not quit.checkForInput(pygame.mouse.get_pos())

   # screen.fill("white")
    for buttons in button_group:
        buttons.update()
        buttons.changeColor(pygame.mouse.get_pos())

    pygame.display.update()

    if game_start:
        Game().run()
        break

pygame.quit()
