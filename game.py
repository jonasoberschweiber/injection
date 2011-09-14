import sys
import pygame
from world import World
from viewport import Viewport
from fighter import Fighter
from pointsbar import PointsBar
from injectionsbar import InjectionsBar
from ai import FightingAi

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
        self.fighter1 = Fighter(self, pygame.Color(0, 0, 200, 255))
        self.fighter2 = Fighter(self, pygame.Color(200, 0, 0, 255))
        self.fighter2.rect.left = 800
        self.pointsbar1 = PointsBar(self.fighter1, pygame.Rect(22, 17, 323, 27), color=1)
        self.pointsbar2 = PointsBar(self.fighter2, pygame.Rect(683, 17, 323, 27), color=2)
        self.injectionsbar1 = InjectionsBar(self.fighter1, pygame.Rect(33, 50, 300, 27))
        self.injectionsbar2 = InjectionsBar(self.fighter2, pygame.Rect(695, 50, 300, 27))
#        self.ai = FightingAi(self, self.fighter2)

        self.f = self.fighter1
    def ev_quit(self, e):
        pass

    def ev_keydown(self, e):
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
        if e.key == pygame.K_LEFT:
            self.f.stop_left()
        elif e.key == pygame.K_RIGHT:
            self.f.stop_right()

    def opponent(self, caller):
        opp = self.fighter2
        if opp == caller:
            opp = self.fighter1
        return opp

    def hit_opponent(self, caller, damage):
        opp = self.opponent(caller)
        opp_hb = opp.hit_boxes()
        direction = 1
        if caller.looking_right:
            direction = -1
        if any([x.collidelist(opp_hb) != -1 for x in caller.hit_boxes()]):
            opp.take_damage(damage, direction)

    def main_loop(self):
        while True:
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
        #    self.ai.update()

            pygame.display.flip()

if __name__ == "__main__":
    Game().main_loop()
