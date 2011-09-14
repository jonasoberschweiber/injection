import pygame

class PointsBar:
    def __init__(self, fighter, rect, color):
        fighter.damage_callbacks.append(self.damage_taken)
        self.fighter = fighter
        self.rect = rect
        self.health = 100
        self.background = pygame.image.load("gfx/hpbar-bg.png")

        if color == 1:
            self.bar = pygame.image.load("gfx/hpbar_blue.png")
        else:
            self.bar = pygame.image.load("gfx/hpbar_red.png")

        self.animation_health = 100
        self.animation = False

    def damage_taken(self, new_health):
        self.animation_health = self.health
        self.health = new_health
        self.animation = True

    def render(self, surface):
        bar_rect = self.rect.move(2, 2)
        bar_rect.width = 323 / 100.0 * self.animation_health

        surface.blit(self.background, self.rect)
        surface.blit(self.bar, bar_rect, area=pygame.Rect(0, 0, bar_rect.width, 21))

        if self.animation:
            self.animation_health -= 2
            if self.animation_health in [self.health, self.health - 1]:
                self.animation = False
