import pygame

class RoundCounter:
    def __init__(self, rect):
        self.rounds = (pygame.image.load("gfx/round1.png"),
                       pygame.image.load("gfx/round2.png"), 
                       pygame.image.load("gfx/round3.png"))
        self.round = 0
        self.rect = rect

    def render(self, surface):
        surface.blit(self.rounds[self.round], self.rect)

    def next_round(self):
        self.round += 1

    def reset(self):
        self.round = 0
