import sys
import pygame
from world import World
from fighter import Fighter

class Game:
    def __init__(self):
        pygame.init()
        pygame.display.set_caption("Injection")
        pygame.key.set_repeat(300, 30)
        self.surface = pygame.display.set_mode((1024, 768), pygame.HWSURFACE | pygame.DOUBLEBUF)
        self.world = World("gfx/bg01.png")
        self.fighter1 = Fighter(self.world)
        self.fighter2 = Fighter(self.world)

    def ev_quit(self, e):
        pass

    def ev_keydown(self, e):
        if e.unicode == 'd':
            self.world.offset = (self.world.offset[0] + 10, self.world.offset[1])
        elif e.unicode == 'a':
            self.world.offset = (self.world.offset[0] - 10, self.world.offset[1])
        elif e.unicode == 'q':
            sys.exit()

    def ev_keyup(self, e):
        pass

    def main_loop(self):
        step_size = 20
        max_frame_time = 100

        now = pygame.time.get_ticks()
        while True:
            for e in pygame.event.get():
                if e.type == pygame.QUIT:
                    self.ev_quit(e)
                elif e.type == pygame.KEYDOWN:
                    self.ev_keydown(e)
                elif e.type == pygame.KEYUP:
                    self.ev_keyup(e)

            T = pygame.time.get_ticks()

            if (T - now) > max_frame_time:
                now = T - step_size

            while (T - now) >= step_size:
                self.fighter1.update()
                self.surface.fill((0, 0, 0))
                self.world.render(self.surface)
                self.fighter1.render(self.surface)
                now += step_size
            else:
                pygame.time.wait(10)

            pygame.display.flip()

if __name__ == "__main__":
    Game().main_loop()
