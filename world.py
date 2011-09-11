import pygame

class World:
    def __init__(self, bgfile):
        self.background = pygame.image.load(bgfile)
        self.offset = (0, 0)
        self.platforms = [((0, 675), (1000, 660))]

    def render(self, surface):
        area = self.background.get_rect()
        area.left = self.offset[0]
        area.top = self.offset[1]

        surface.blit(self.background, (0, 0), area)
