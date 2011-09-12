import sys
import pygame
from world import World
from viewport import Viewport
from fighter import Fighter
from pointsbar import PointsBar

class Game:
    def __init__(self):
        pygame.init()
        pygame.display.set_caption("Injection")
        self.clock = pygame.time.Clock()
        self.surface = pygame.display.set_mode((1024, 768), pygame.HWSURFACE | pygame.DOUBLEBUF)
        self.viewport = Viewport(self)
        self.world = World(self, "gfx/world01.json")
        self.fighter1 = Fighter(self, pygame.Color(200, 0, 0, 255))
        self.fighter2 = Fighter(self, pygame.Color(0, 0, 200, 255))
        self.fighter2.rect.left = 800
        self.pointsbar1 = PointsBar(self.fighter1, pygame.Rect(20, 20, 250, 30), pygame.Color(200, 0, 0, 255))
        self.pointsbar2 = PointsBar(self.fighter2, pygame.Rect(750, 20, 250, 30), pygame.Color(0, 0, 200, 255))

        self.f = self.fighter1
    def ev_quit(self, e):
        pass

    def ev_keydown(self, e):
        if e.unicode == 'd':
            self.f.right()
        elif e.unicode == 'a':
            self.f.left()
        elif e.unicode == 'w':
            self.f.jump()
        elif e.unicode == 'j':
            self.f.punch()
        elif e.unicode == 'k':
            self.f.kick()
        elif e.unicode == 's':
            if self.f == self.fighter1:
                self.f = self.fighter2
            else:
                self.f = self.fighter1
        elif e.unicode == 'q':
            sys.exit()

    def ev_keyup(self, e):
        if e.key == 97:
            self.f.stop_left()
        elif e.key == 100:
            self.f.stop_right()

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

            pygame.display.flip()

if __name__ == "__main__":
    Game().main_loop()
