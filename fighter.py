import pygame
import util

from spritemap import SpriteMap

class Fighter(pygame.sprite.Sprite):
    def __init__(self, world):
        pygame.sprite.Sprite.__init__(self)
        self.world = world
        self.color = pygame.Color(200, 0, 0, 255)
        self.sprite_map = SpriteMap('gfx/fighter.json', filter=util.create_colorizer(self.color))
        self.rect = pygame.Rect(0, 0, 128, 256)

    def render(self, surface):
        surface.blit(self.sprite_map.image(), self.rect, area=self.sprite_map.sprite_rect('still'))

    def update(self):
        for platform in self.world.platforms:
            platform_rect = pygame.Rect(platform[0][0], platform[0][1],
                                        platform[1][0] - platform[0][0], platform[1][1] - platform[0][1])
            
            if not self.rect.colliderect(platform_rect):
                self.rect = self.rect.move(0, 5)

            collide_left = self.rect.left > platform[0][0]
            collide_right = self.rect.left + self.rect.width < platform[1][0]
            collide_top = self.rect.top + self.rect.height > platform[0][1] and self.rect.top + self.rect.height < platform[0][1] + 1
