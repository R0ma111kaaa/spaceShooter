import pygame
import sys



from game import Game
from level3 import start_level3
pygame.init()
Back_Ground = pygame.image.load("data/Design_menu/spacebackground.png")  # Back groundwz
screen = pygame.display.set_mode()
main_font = pygame.font.Font("data/Design_menu/font.ttf", 45)
Button_design = pygame.image.load("data/Design_menu/button2.png")





class Main_Menu:
    def __init__(self, screen, Back_Ground, Button_design):
        self.clock = pygame.time.Clock()
        self.screen = screen
        # design
        self.Back_Ground = pygame.transform.scale(Back_Ground, (screen.get_width(), screen.get_height()))
        self.button_surface = Button_design  # pygame.image.load("data/Design_menu/button2.png")
        self.button_surface = pygame.transform.scale(self.button_surface, (600, 200))

        self.start_bt = Button(self.button_surface, self.screen.get_width() // 2, 200, "Start Game", main_font)
        #self.level_editor_bt = Button(self.button_surface, self.screen.get_width() // 2, 400, "Level Editor", main_font)
        self.help_bt = Button(self.button_surface, self.screen.get_width() // 2, 400, "Help", main_font)
        self.quit_bt = Button(self.button_surface, self.screen.get_width() // 2, 600, "Exit", main_font)
        self.button_group = [self.start_bt, self.help_bt, self.quit_bt, ] # self.level_editor_bt
        # конец design
        exit = True
        while exit:
            self.screen.blit(self.Back_Ground, (0, 0))
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()
                if event.type == pygame.MOUSEBUTTONDOWN:
                    if self.start_bt.checkForInput(pygame.mouse.get_pos()):  # вход в левел селект
                        self.level_select()
                    if self.help_bt.checkForInput(pygame.mouse.get_pos()):
                        self.help()
                    exit = not self.quit_bt.checkForInput(pygame.mouse.get_pos())

            # screen.fill("white")
            for buttons in self.button_group:
                buttons.update()
                buttons.changeColor(pygame.mouse.get_pos())

            pygame.display.update()

            #  level_select(self)
            # Game().run()
        pygame.quit()

    def level_select(self):
        # design
        level_bt_design = pygame.image.load("data/Design_menu/level_button.png")
        level_clear = pygame.transform.scale(pygame.image.load("data/Design_menu/level_button.png"), (500, 500))
        level_bt_design = pygame.transform.scale(level_bt_design, (500, 500))
        level1_bt = Button(level_bt_design, int(self.screen.get_width() * 0.2), 250, "level 1", main_font)
        level2_bt = Button(level_bt_design, int(self.screen.get_width() * 0.5), 250, "level 2", main_font)
        level3_bt = Button(level_bt_design, int(self.screen.get_width() * 0.8), 250, "level 3", main_font)
        exit = Button(level_bt_design, self.screen.get_width() // 2, int(self.screen.get_height() * 0.9), "exit",
                      main_font)
        level_bt_group = [level1_bt, level2_bt, level3_bt, exit]
        # end design
        exit2 = True
        while exit2:
            self.screen.blit(self.Back_Ground, (0, 0))
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()
                if event.type == pygame.MOUSEBUTTONDOWN:
                    if level1_bt.checkForInput(pygame.mouse.get_pos()):
                        Game(0).run()
                    if level2_bt.checkForInput(pygame.mouse.get_pos()):
                        Game(1).run()
                    if level3_bt.checkForInput(pygame.mouse.get_pos()):
                        start_level3()
                    if exit.checkForInput(pygame.mouse.get_pos()):
                        exit2 = False  # not exit.checkForInput(pygame.mouse.get_pos())
            for buttons in level_bt_group:
                buttons.update()
                buttons.changeColor(pygame.mouse.get_pos())
            pygame.display.update()

    def help(self):
        # design
        text1 = main_font.render("Movement: W A S D", True,
                                 (255, 255, 255))  # ["Movement:  W A S D", "Shoot: Space Bar"]
        text2 = main_font.render("Dash: space bar", True, (255, 255, 255))
        text3 = main_font.render("Goal: kill all enemies", True, (255, 255, 255))
        text = [text1, text2, text3]
        exit = Button(self.button_surface, self.screen.get_width() // 2, int(self.screen.get_height() * 0.9), "exit",
                      main_font)
        # end design
        running = True
        while running:
            screen.blit(self.Back_Ground, (0, 0))
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()
                if event.type == pygame.MOUSEBUTTONDOWN:
                    running = not exit.checkForInput(pygame.mouse.get_pos())
            y = self.screen.get_height() * 0.1
            for elem in text:
                screen.blit(elem, (int(self.screen.get_width() * 0.1), y))
                y += elem.get_height() + 20
            exit.update()
            exit.changeColor(pygame.mouse.get_pos())
            pygame.display.update()
        # text = "Movement w a s d"
        # end design

    def draw_text(self, *text, color=(255, 255, 255)):
        # screen.blit(self.Back_Ground, (0,0))
        text_x = int(self.screen.get_width() // 2 * 0.2)
        text_y = int(self.screen.get_height() // 2 * 0.1)
        for line in text:
            final = main_font.render(line, True, color)
            text_y = self.screen.get_height() // 2 + final.get_height() // 2
            screen.blit(final, (text_x, text_y))


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




if __name__ == '__main__':
    Main_Menu(screen, Back_Ground, Button_design)
