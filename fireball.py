import pygame

FIREBALL_SPEED = 30
FIGHTER_OFFSET_Y = 100
FIREBALL_DAMAGE = 90

class Fireball:
    def __init__(self, game, fighter):
        self.game = game
        self.fighter = fighter

        self.big = pygame.image.load('gfx/fireball01.png').convert_alpha()
        self.slim = pygame.image.load('gfx/fireball02.png').convert_alpha()

        self.image = self.big

        self.pos = (fighter.rect.x, fighter.rect.y + FIGHTER_OFFSET_Y)

        self.speed = FIREBALL_SPEED
        self.looking_right = fighter.looking_right
        if not self.looking_right:
            self.speed = -self.speed
            self.big = pygame.transform.flip(self.big, True, False)
            self.slim = pygame.transform.flip(self.slim, True, False)

        self.frame = 0

    def render(self, surface):
        r = self.game.viewport.real_rect(pygame.Rect(self.pos[0], self.pos[1],
            self.image.get_width(), self.image.get_height()))
        surface.blit(self.image, r)
    
    def update(self):
        self.pos = (self.pos[0] + self.speed, self.pos[1])

        if self.frame == 2:
            self.image = self.slim
        
        self.frame += 1

        if self.pos[0] > self.game.world.rect.width:
            self.game.fireballs.remove(self)
            return

        if self.game.hit_opponent(self.fighter, FIREBALL_DAMAGE, [pygame.Rect(self.pos[0], self.pos[1],
            self.image.get_width(), self.image.get_height())], kind='magical'):
            self.game.fireballs.remove(self)
