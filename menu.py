import sys
import pygame

class MainMenu:
    def __init__(self, m):
        self.m = m
        self.img_title = pygame.image.load("gfx/menu_title.png")
        self.img_singleplayer = (pygame.image.load("gfx/btn_singleplayer.png"), pygame.image.load("gfx/btn_singleplayer_inactive.png"))
        self.img_multiplayer = (pygame.image.load("gfx/btn_multiplayer.png"), pygame.image.load("gfx/btn_multiplayer_inactive.png"))
        self.img_help = (pygame.image.load("gfx/btn_help.png"), pygame.image.load("gfx/btn_help_inactive.png"))
        self.img_exit = (pygame.image.load("gfx/btn_exit.png"), pygame.image.load("gfx/btn_exit_inactive.png"))

        self.buttons = [(self.img_singleplayer, self.btn_singleplayer),
                        (self.img_multiplayer, self.btn_multiplayer),
                        (self.img_help, self.btn_help), 
                        (self.img_exit, self.btn_exit)]
        self.current_button = 0
        self.rect = pygame.Rect(390, 185, 248, 50)

    def key_press(self, key):
        if key == pygame.K_DOWN:
            if self.current_button < len(self.buttons) - 1:
                self.current_button += 1
        elif key == pygame.K_UP:
            if self.current_button > 0:
                self.current_button -= 1
        elif key == pygame.K_RETURN or key == pygame.K_SPACE or key == pygame.K_RIGHT:
            self.buttons[self.current_button][1]()

    def render(self):
        self.m.surface.fill(pygame.Color(255, 255, 255))
        self.m.surface.blit(self.img_title, (350, 45))
        for i in range(0, len(self.buttons)):
            if i == self.current_button:
                self.m.surface.blit(self.buttons[i][0][0], self.rect.move(0, i*70))
            else:
                self.m.surface.blit(self.buttons[i][0][1], self.rect.move(0, i*70))

    def btn_singleplayer(self):
        self.m.active = False
        self.m.game.next_round()
            
    def btn_multiplayer(self):
        self.m.active = False

    def btn_help(self):
        self.m.current_menu = 1

    def btn_exit(self):
        sys.exit()
    
class HelpMenu:
    def __init__(self, m):
        self.m = m
        self.help_image = pygame.image.load("gfx/injections.png")
        self.rect = self.help_image.get_rect()

    def key_press(self, key):
        if key == pygame.K_DOWN:
            if self.rect.bottom > 768:
                self.rect = self.rect.move(0, -40)
        elif key == pygame.K_UP:
            if self.rect.top < 0:
                self.rect = self.rect.move(0, 40)
        elif key == pygame.K_LEFT or key == pygame.K_RETURN or key == pygame.K_SPACE:
            self.m.current_menu = 0

    def render(self):
        self.m.surface.fill(pygame.Color(255, 255, 255))
        self.m.surface.blit(self.help_image, self.rect)

class Menu:
    def __init__(self, game):
        self.game = game
        self.active = True
        self.menus = [MainMenu(self), HelpMenu(self)]
        self.current_menu = 0
        self.surface = pygame.display.get_surface()

    def key_press(self, key):
        self.menus[self.current_menu].key_press(key)

    def loop(self):
        pygame.key.set_repeat(200, 30)
        while True:
            for e in pygame.event.get():
                if e.type == pygame.KEYDOWN:
                    self.key_press(e.key)
            self.render()
            pygame.display.flip()
            if not self.active:
                break
        pygame.key.set_repeat(0)

    def render(self):
        self.menus[self.current_menu].render()
