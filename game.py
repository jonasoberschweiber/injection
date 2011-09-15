import sys
import pygame
from world import World
from viewport import Viewport
from fighter import Fighter
from pointsbar import PointsBar
from injectionsbar import InjectionsBar
from roundcounter import RoundCounter
from ai import FightingAi
from menu import Menu

class Game:
    def __init__(self):
        pygame.mixer.pre_init(frequency=22050, size=-16, channels=8, buffer=256)
        pygame.init()
        pygame.display.set_caption("Injection")
        pygame.mixer.init()
        self.clock = pygame.time.Clock()
        self.surface = pygame.display.set_mode((1024, 768), pygame.HWSURFACE | pygame.DOUBLEBUF)
        self.viewport = Viewport(self)
        self.world = World(self, "gfx/world01.json")
        self.fighter1 = Fighter(self, pygame.Color(0, 0, 200, 255), startpos=(50, 0))
        self.fighter2 = Fighter(self, pygame.Color(200, 0, 0, 255), startpos=(850, 0))
        self.fighter2.rect.left = 800
        self.pointsbar1 = PointsBar(self.fighter1, pygame.Rect(22, 17, 323, 27), color=1)
        self.pointsbar2 = PointsBar(self.fighter2, pygame.Rect(683, 17, 323, 27), color=2)
        self.injectionsbar1 = InjectionsBar(self.fighter1, pygame.Rect(33, 50, 300, 27))
        self.injectionsbar2 = InjectionsBar(self.fighter2, pygame.Rect(695, 50, 300, 27))
        self.roundcounter = RoundCounter(self, pygame.Rect(427, 0, 167, 50))
        self.ai = FightingAi(self, self.fighter2)
        self.menu = Menu(self)
        self.ignore_keys = False

        self.fireballs = []
        pygame.mixer.music.load("snd/music.wav")
        pygame.mixer.music.set_volume(.35)
        #pygame.mixer.music.set_volume(0)
        pygame.mixer.music.play()
        self.f = self.fighter1
    def ev_quit(self, e):
        pass

    def ev_keydown(self, e):
        if self.ignore_keys:
            return

        if e.key == pygame.K_RIGHT:
            self.f.right()
        elif e.key == pygame.K_LEFT:
            self.f.left()
        elif e.key == pygame.K_SPACE:
            self.f.jump()
        elif e.unicode == 'm':
            self.f.punch()
        elif e.unicode == 'n':
            self.f.kick()
        elif e.key == pygame.K_UP:
            if self.f.current_injection < len(self.f.injections) - 1:
                self.f.switch_to_injection(self.f.current_injection + 1)
        elif e.unicode == 's':
            if self.f == self.fighter1:
                self.f = self.fighter2
            else:
                self.f = self.fighter1
        elif e.unicode == 'q':
            sys.exit()

    def ev_keyup(self, e):
        if self.ignore_keys:
            return

        if e.key == pygame.K_LEFT:
            self.f.stop_left()
        elif e.key == pygame.K_RIGHT:
            self.f.stop_right()

    def opponent(self, caller):
        opp = self.fighter2
        if opp == caller:
            opp = self.fighter1
        return opp

    def hit_opponent(self, caller, damage, hit_boxes=None):
        opp = self.opponent(caller)
        opp_hb = opp.hit_boxes()
        direction = 1
        if caller.looking_right:
            direction = -1
        if hit_boxes == None:
            hit_boxes = caller.hit_boxes()
        if any([x.collidelist(opp_hb) != -1 for x in hit_boxes]):
            opp.take_damage(damage, direction)
            return True
        return False

    def game_over(self):
        print "GAME OVER"

    def next_round(self):
        if self.roundcounter.round < len(self.roundcounter.rounds) - 1:
            self.fighter1.reset()
            self.fighter2.reset()
            self.ai.reset()
            for inj in self.injectionsbar1.injections[1:]:
                inj.disabled = False
                inj.activate = False
            for inj in self.injectionsbar2.injections[1:]:
                inj.disabled = False
                inj.activate = False
            self.pointsbar1.health = self.fighter1.health
            self.pointsbar2.health = self.fighter2.health
            self.viewport.offset = 0
            self.roundcounter.next_round()
        else:
            self.game_over()

    def check_state(self):
        if self.fighter1.health <= 0:
            self.fighter2.wins += 1
            self.next_round()
        if self.fighter2.health <= 0:
            self.fighter1.wins += 1
            self.next_round()
        

    def main_loop(self):
        while True:
            if self.menu.active:
                self.menu.loop()

            self.clock.tick(30)
            for e in pygame.event.get():
                if e.type == pygame.QUIT:
                    self.ev_quit(e)
                elif e.type == pygame.KEYDOWN:
                    self.ev_keydown(e)
                elif e.type == pygame.KEYUP:
                    self.ev_keyup(e)

            self.fighter1.update()
            self.fighter2.update()
            self.surface.fill((0, 0, 0))
            self.world.render(self.surface)
            self.fighter1.render(self.surface)
            self.fighter2.render(self.surface)
            self.pointsbar1.render(self.surface)
            self.pointsbar2.render(self.surface)
            self.injectionsbar1.render(self.surface)
            self.injectionsbar2.render(self.surface)
            self.roundcounter.render(self.surface)
            #self.ai.update()

            for f in self.fireballs:
                f.update()
                f.render(self.surface)

            pygame.display.flip()

if __name__ == "__main__":
    Game().main_loop()
