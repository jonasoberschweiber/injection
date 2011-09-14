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
        self.num_font = pygame.font.Font(pygame.font.get_default_font(), 16)
        self.num_color = pygame.Color(255, 0, 0)

        self.animation_health = 100
        self.animation = False
        self.num_animation = 0
        self.num = 0

    def damage_taken(self, new_health, dmg):
        self.animation_health = self.health
        self.health = new_health
        self.animation = True
        self.num_animation = 1
        self.num = -1*dmg
        self.num_rect = self.fighter.real_rect().move(34, 80)

    def render(self, surface):
        bar_rect = self.rect.move(2, 2)
        bar_rect.width = 323 / 100.0 * self.animation_health

        surface.blit(self.background, self.rect)
        surface.blit(self.bar, bar_rect, area=pygame.Rect(0, 0, bar_rect.width, 21))

        if self.animation:
            self.animation_health -= 2
            if self.animation_health in [self.health, self.health - 1]:
                self.animation = False

        if self.num_animation > 0:
            surface.blit(self.num_font.render(str(self.num), 1, self.num_color), self.num_rect)
            self.num_rect = self.num_rect.move(0, -5)
            self.num_animation += 1
            if self.num_animation == 20:
                self.num_animation = 0
