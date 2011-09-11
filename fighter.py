import pygame
import util

class Fighter(pygame.sprite.Sprite):
    def __init__(self, world):
        pygame.sprite.Sprite.__init__(self)
        self.world = world
        self.color = pygame.Color(200, 0, 0, 255)
        self.image = util.colorize_image(pygame.image.load("gfx/still01.png"), self.color)
        self.rect = self.image.get_rect()

    def render(self, surface):
        surface.blit(self.image, self.rect)

    def update(self):
        for platform in self.world.platforms:
            platform_rect = pygame.Rect(platform[0][0], platform[0][1],
                                        platform[1][0] - platform[0][0], platform[1][1] - platform[0][1])
            
            if not self.rect.colliderect(platform_rect):
                self.rect = self.rect.move(0, 10)
