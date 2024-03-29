import sys
import pygame
from mutation import *

class MainMenu:
    def __init__(self, m, game=None):
        self.m = m
        self.game = game
        self.img_title = pygame.image.load("gfx/menu_title.png").convert_alpha()
        self.img_singleplayer = (pygame.image.load("gfx/btn_singleplayer.png").convert_alpha(), pygame.image.load("gfx/btn_singleplayer_inactive.png").convert_alpha())
        self.img_multiplayer = (pygame.image.load("gfx/btn_multiplayer.png").convert_alpha(), pygame.image.load("gfx/btn_multiplayer_inactive.png").convert_alpha())
        self.img_help = (pygame.image.load("gfx/btn_help.png").convert_alpha(), pygame.image.load("gfx/btn_help_inactive.png").convert_alpha())
        self.img_exit = (pygame.image.load("gfx/btn_exit.png").convert_alpha(), pygame.image.load("gfx/btn_exit_inactive.png").convert_alpha())

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
            elif self.current_button == len(self.buttons) - 1:
                self.current_button = 0
        elif key == pygame.K_UP:
            if self.current_button > 0:
                self.current_button -= 1
            elif self.current_button == 0:
                self.current_button = len(self.buttons) - 1
        elif key == pygame.K_RETURN or key == pygame.K_SPACE or key == pygame.K_RIGHT:
            self.buttons[self.current_button][1]()
    
    def reset(self):
        pass

    def render(self):
        self.m.surface.fill(pygame.Color(255, 255, 255))
        self.m.surface.blit(self.img_title, (350, 45))
        for i in range(0, len(self.buttons)):
            if i == self.current_button:
                self.m.surface.blit(self.buttons[i][0][0], self.rect.move(0, i*70))
            else:
                self.m.surface.blit(self.buttons[i][0][1], self.rect.move(0, i*70))

    def btn_singleplayer(self):
        self.game.fighter2.randomize_injections()
        self.m.current_menu = 2
            
    def btn_multiplayer(self):
        self.m.current_menu = 3

    def btn_help(self):
        self.m.current_menu = 1

    def btn_exit(self):
        sys.exit()
    
class HelpMenu:
    def __init__(self, m):
        self.m = m
        self.help_image = pygame.image.load("gfx/instructions.png").convert_alpha()
        self.rect = self.help_image.get_rect()
    
    def reset(self):
        pass

    def key_press(self, key):
        if key == pygame.K_DOWN:
            if self.rect.bottom > 768:
                self.rect = self.rect.move(0, -40)
        elif key == pygame.K_UP:
            if self.rect.top < 0:
                self.rect = self.rect.move(0, 40)
        elif key in [pygame.K_LEFT, pygame.K_SPACE, pygame.K_ESCAPE]:
            self.m.current_menu = 0

    def render(self):
        self.m.surface.fill(pygame.Color(255, 255, 255))
        self.m.surface.blit(self.help_image, self.rect)

class InjectionMenu:
    def __init__(self, m, game=None, multiplayer=0):
        self.m = m
        self.game = game
        self.available_injections = [SwiftFeetMutation(), HardenedSkinMutation(), StrengthMutation(), 
                                     MagicalAffinityMutation(), WingsMutation(), TranquilityMutation(), 
                                     ToxicMutation()]
        self.selection1 = 0
        self.selection2 = 0
        self.img_avail_inj = pygame.image.load("gfx/injmenu/available_injections.png").convert_alpha()
        self.img_your_inj = pygame.image.load("gfx/injmenu/yourinjections.png").convert_alpha()
        self.img_ready = pygame.image.load("gfx/injmenu/ready.png").convert_alpha()
        self.img_selection = pygame.image.load("gfx/injmenu/selection.png").convert_alpha()
        self.img_mut_separator = pygame.image.load("gfx/mutation_separator.png").convert_alpha()
        self.img_keys = pygame.image.load("gfx/injmenu/keys.png").convert_alpha()
        self.injections_rect1 = pygame.Rect(50, 130, 0, 0)
        self.injections_rect2 = pygame.Rect(565, 130, 0, 0)
        self.player1_mutations = []
        self.player2_mutations = []
        self.player1_mutationsrect = pygame.Rect(50, 560, 0, 0)
        self.player2_mutationsrect = pygame.Rect(565, 560, 0, 0)
        self.player1_avail_injrect = pygame.Rect(50, 50, 0, 0)
        self.player2_avail_injrect = pygame.Rect(565, 50, 0, 0)
        self.player1_your_injrect = pygame.Rect(50, 500, 0, 0)
        self.player2_your_injrect = pygame.Rect(565, 500, 0, 0)
        self.player1_readyrect = pygame.Rect(50, 635, 0, 0)
        self.player2_readyrect = pygame.Rect(565, 635, 0, 0)
        self.keys_rect = pygame.Rect(337, 685, 0, 0)
        self.multiplayer = multiplayer

    def selection_left(self, player=1):
        if player == 1:
            if self.selection1 % 3 != 0:
                self.selection1 -= 1
        else:
            if self.selection2 % 3 != 0:
                self.selection2 -= 1

    def selection_up(self, player=1):
        if player == 1:
            if self.selection1 >= 3:
                self.selection1 -= 3
        else:
            if self.selection2 >= 3:
                self.selection2 -= 3
            
    def selection_right(self, player=1):
        if player == 1:
            if self.selection1 % 3 != 2 and self.selection1 < len(self.available_injections) - 1:
                self.selection1 += 1
        else:
            if self.selection2 % 3 != 2 and self.selection2 < len(self.available_injections) - 1:
                self.selection2 += 1

    def selection_down(self, player=1):
        if player == 1:
            if self.selection1 < len(self.available_injections) - 3:
                self.selection1 += 3
        else:
            if self.selection2 < len(self.available_injections) - 3:
                self.selection2 += 3

    def add_mutation(self, player=1):
        if player == 1:
            self.player1_mutations.append(self.available_injections[self.selection1])
        else:
            self.player2_mutations.append(self.available_injections[self.selection2])

    def delete_mutation(self, player=1):
        if player == 1:
            self.player1_mutations= self.player1_mutations[:-1]
        else:
            self.player2_mutations= self.player2_mutations[:-1]

    def key_press(self, key):
        # Fighter 2
        if self.multiplayer:
            if key == pygame.K_LEFT:
                self.selection_left(player=2)
            elif key == pygame.K_RIGHT:
                self.selection_right(player=2)
            elif key == pygame.K_UP:
                self.selection_up(player=2)
            elif key == pygame.K_DOWN:
                self.selection_down(player=2)
            elif key == pygame.K_SLASH:
                if len(self.player2_mutations) < 6:
                    self.add_mutation(player=2)
                self.check_state()
            elif key == pygame.K_PERIOD:
                self.delete_mutation(player=2)

        # Fighter 1
        if key == pygame.K_a:
            self.selection_left(player=1)
        elif key == pygame.K_d:
            self.selection_right(player=1)
        elif key == pygame.K_w:
            self.selection_up(player=1)
        elif key == pygame.K_s:
            self.selection_down(player=1)
        elif key == pygame.K_j:
            if len(self.player1_mutations) < 6:
                self.add_mutation(player=1)
            self.check_state()
        elif key == pygame.K_h:
            self.delete_mutation(player=1)

        elif key == pygame.K_ESCAPE:
            self.reset()
            self.m.current_menu = 0

    def reset(self):
        self.player1_mutations = []
        self.player2_mutations = []
        if not self.multiplayer:
            for m in self.game.fighter2.injections:
                self.player2_mutations.append(m[0])
                self.player2_mutations.append(m[1])
        self.selection1 = 0
        self.selection2 = 0

    def check_state(self):
        print len(self.player2_mutations)
        if len(self.player1_mutations) == 6 and len(self.player2_mutations) == 6:
            self.m.game.fighter1.injections = []
            for i in range(0, len(self.player1_mutations)):
                if i % 2:
                    self.m.game.fighter1.injections.append((tmp_mutation, self.player1_mutations[i], None))
                else:
                    tmp_mutation = self.player1_mutations[i]
            if self.multiplayer:
                self.m.game.fighter2.injections = []
                for i in range(0, len(self.player2_mutations)):
                    if i % 2:
                        self.m.game.fighter2.injections.append((tmp_mutation, self.player2_mutations[i], None))
                    else:
                        tmp_mutation = self.player2_mutations[i]
    
            self.m.game.multiplayer = self.multiplayer
            self.m.start_game()
    
    def render_mutations(self, mut, mutrect, sel):
        for i in range(0, len(mut) + 1):
            if i % 2:
                if i > len(mut) - 1:
                    self.m.surface.blit(self.available_injections[sel].image_right_inactive, mutrect.move(32*i, 0))
                    self.m.surface.blit(self.img_mut_separator, mutrect.move(32*i - 1, 0))
                    continue
                self.m.surface.blit(mut[i].image_right, mutrect.move(32*i, 0))
                self.m.surface.blit(self.img_mut_separator, mutrect.move(32*i - 1, 0))
            else:
                if i > len(mut) - 1:
                    if i < 6:
                        self.m.surface.blit(self.available_injections[sel].image_left_inactive, mutrect.move(32*i, 0))
                    continue
                self.m.surface.blit(mut[i].image_left, mutrect.move(32*i, 0))


    def render(self):
        self.m.surface.fill(pygame.Color(255, 255, 255))
        for i in range(0, len(self.available_injections)):
            self.m.surface.blit(self.available_injections[i].image_full, self.injections_rect1.move(125*(i%3), 110*(i/3)))
            self.m.surface.blit(self.available_injections[i].image_full, self.injections_rect2.move(125*(i%3), 110*(i/3)))
            if i == self.selection1:
                if len(self.player1_mutations) < 6:
                    self.m.surface.blit(self.img_selection, self.injections_rect1.move(125*(i%3) - 10, 110*(i/3) - 10))
            if i == self.selection2:
                if len(self.player2_mutations) < 6:
                    self.m.surface.blit(self.img_selection, self.injections_rect2.move(125*(i%3) - 10, 110*(i/3) - 10))
        
        self.render_mutations(self.player1_mutations, self.player1_mutationsrect, self.selection1)
        self.render_mutations(self.player2_mutations, self.player2_mutationsrect, self.selection2)

        self.m.surface.blit(self.img_avail_inj, self.player1_avail_injrect)
        self.m.surface.blit(self.img_avail_inj, self.player2_avail_injrect)
        self.m.surface.blit(self.img_your_inj, self.player1_your_injrect)
        self.m.surface.blit(self.img_your_inj, self.player2_your_injrect)
        self.m.surface.blit(self.img_keys, self.keys_rect)
        if len(self.player1_mutations) == 6:
            self.m.surface.blit(self.img_ready, self.player1_readyrect)
        if len(self.player2_mutations) == 6:
            self.m.surface.blit(self.img_ready, self.player2_readyrect)
        

class Menu:
    def __init__(self, game):
        self.game = game
        self.active = True
        self.menus = [MainMenu(self, game), HelpMenu(self), InjectionMenu(self, game), InjectionMenu(self, game, 1)]
        self.current_menu = 0
        self.surface = pygame.display.get_surface()

    def key_press(self, key):
        self.menus[self.current_menu].key_press(key)
    
    def __setattr__(self, name, value):
        self.__dict__[name] = value
        if name == 'current_menu':
            self.menus[self.current_menu].reset()

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

    def start_game(self):
        self.active = False
        self.game.injectionsbar1.update_injections()
        self.game.injectionsbar2.update_injections()
        self.game.next_round()

    def render(self):
        self.menus[self.current_menu].render()

    def activate(self):
        self.active = True
        self.current_menu = 0
