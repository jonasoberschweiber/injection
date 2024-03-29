import pygame

class PointsBar:
    def __init__(self, fighter, rect, color):
        fighter.damage_callbacks.append(self.damage_taken)
        fighter.health_callbacks.append(self.health_increased)
        self.fighter = fighter
        self.rect = rect
        self.health = 1000
        self.background = pygame.image.load("gfx/hpbar-bg.png").convert_alpha()

        if color == 1:
            self.bar = pygame.image.load("gfx/hpbar_blue.png").convert_alpha()
        else:
            self.bar = pygame.image.load("gfx/hpbar_red.png").convert_alpha()
        self.num_font = pygame.font.Font("gfx/intuitive.ttf", 24)
        self.num_color = pygame.Color(255, 0, 0)
        self.gain_color = pygame.Color(0, 255, 0)
        self.resisted_color = pygame.Color(200, 200, 10)

        self.animation_health = 1000
        self.animation = False
        self.num_animation = 0
        self.num = 0
    
    def health_increased(self, new_health, inc):
        self.num_animation = 1
        self.num = inc
        self.num_rect = self.fighter.real_rect().move(34, 80)
        self.animation = True
        self.animation_health = self.health
        self.health = new_health

    def damage_taken(self, new_health, dmg, kind):
        self.health = new_health
        self.animation = True
        self.num_animation = 1
        self.num = -1*dmg
        self.num_rect = self.fighter.real_rect().move(34, 80)

    def render(self, surface):
        bar_rect = self.rect.move(2, 2)
        bar_rect.width = 323 / 1000.0 * self.animation_health

        surface.blit(self.background, self.rect)
        surface.blit(self.bar, bar_rect, area=pygame.Rect(0, 0, bar_rect.width, 21))

        if self.animation:
            if self.num > 0:
                self.animation_health += 20
                self.animation = self.animation_health < self.health
            else:
                self.animation_health -= 20
                self.animation = self.animation_health > self.health
        if not self.animation:
            self.animation_health = self.health

        if self.num_animation > 0:
            color = self.num_color
            if self.num == 0:
                color = self.resisted_color
                self.num = "Resisted"
            elif self.num > 0:
                color = self.gain_color
            surface.blit(self.num_font.render(str(self.num), 1, color), self.fighter.real_rect().move(34, 80 - self.num_animation*5))
            self.num_rect = self.num_rect.move(0, -5)
            self.num_animation += 1
            if self.num_animation == 20:
                self.num_animation = 0
