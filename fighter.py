import pygame
import util

from spritemap import SpriteMap

class Fighter(pygame.sprite.Sprite):
    def __init__(self, world):
        pygame.sprite.Sprite.__init__(self)
        self.world = world
        self.color = pygame.Color(200, 0, 0, 255)
        self.sprite_map = SpriteMap('gfx/fighter.json')
        self.rect = pygame.Rect(0, 0, 128, 256)
        self.sprite = 'still'

        self.punching = False
        self.anim_frame = 0

    def render(self, surface):
        surface.blit(self.sprite_map.image(), self.rect, area=self.sprite_map.sprite_rect(self.sprite))

    def update(self):
        dy = 60 
        for platform in self.world.platforms:
            platform_rect = pygame.Rect(platform[0][0], platform[0][1],
                                        platform[1][0] - platform[0][0], platform[1][1] - platform[0][1])
            #if not self.rect.colliderect(platform_rect):
            if not util.collide_line_top(self.rect, platform):
                dy = min(dy, abs(self.rect.bottom - platform[0][1]))
            else:
                dy = 0
        self.rect = self.rect.move(0, dy)

        if self.punching:
            if self.anim_frame == 0:
                self.sprite = 'punch02'
            elif self.anim_frame == 2:
                self.sprite = 'punch03'
            elif self.anim_frame >= 6:
                self.sprite = 'still'
                self.punching = False
        
        self.anim_frame += 1

    def punch(self):
        self.punching = True
        self.anim_frame = 0
