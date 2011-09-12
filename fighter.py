import math
import pygame
import util

from spritemap import SpriteMap

JUMP_SPEED = -100
JUMP_DURATION = 15

KICK_DAMAGE = 10
PUNCH_DAMAGE = 5

class Fighter(pygame.sprite.Sprite):
    def __init__(self, world):
        pygame.sprite.Sprite.__init__(self)
        self.world = world
        self.color = pygame.Color(200, 0, 0, 255)
        self.sprite_map = SpriteMap('gfx/fighter.json', filter=util.create_colorizer(self.color))
        self.rect = pygame.Rect(0, 0, 128, 256)
        self.sprite = 'still'
        self.speed_x = 0
        self.speed_y = 0
        self.looking_right = True

        self.health = 100
        self.punching = False
        self.kicking = False
        self.anim_frame = 0
        self.jump_frame = 0

    def render(self, surface):
        off = self.sprite_map.offset(self.sprite)
        rect = self.rect
        if off != 0:
            rect = pygame.Rect(rect.x - off, rect.y, rect.w + off, rect.h)
        surface.blit(self.sprite_map.image(), rect, area=self.sprite_map.sprite_rect(self.sprite))

    def mask(self):
        return self.sprite_map.mask(self.sprite)
    
    def _hit_boxes(self, rect):
        return [x.move(rect.x, rect.y) for x in self.mask().get_bounding_rects()]
    
    def hit_boxes(self):
        return self._hit_boxes(self.rect)

    def update(self):
        dy = 60
        for platform in self.world.adjusted_platforms():
            if not util.collide_line_top(self.rect, platform):
                if self.rect.right > platform[0][0] and self.rect.left < platform[1][0]:
                    dy = min(dy, abs(self.rect.bottom - platform[0][1]))
            else:
                dy = 0
        dy += math.trunc(JUMP_SPEED * math.cos((math.pi / (2 * JUMP_DURATION)) * min(self.jump_frame, JUMP_DURATION)))
        new_rect = self.rect.move(self.speed_x, dy)

        if (not self.world.collides_opponent(self, self._hit_boxes(new_rect))
            and self.world.contains_point((new_rect.left, new_rect.top))):
            if new_rect.left < 0 or new_rect.right > 1024:
                self.world.scroll(self.speed_x)
                new_rect.left -= self.speed_x
            self.rect = new_rect

        if self.speed_x != 0 and not self.punching and not self.kicking:
            if self.anim_frame >= 4:
                self.sprite = 'walk01'
            if self.anim_frame >= 8:
                self.sprite = 'still'
                self.anim_frame = 0

        if self.punching:
            if self.anim_frame == 0:
                self.sprite = 'punch02'
            elif self.anim_frame == 2:
                self.sprite = 'punch03'
                self.world.hit_opponent(self, PUNCH_DAMAGE)
            elif self.anim_frame >= 6:
                self.sprite = 'still'
                self.punching = False

        if self.kicking:
            if self.anim_frame == 0:
                self.sprite = 'kick02'
            elif self.anim_frame == 3:
                self.sprite = 'kick03'
                self.world.hit_opponent(self, KICK_DAMAGE)
            elif self.anim_frame >= 8:
                self.sprite = 'still'
                self.kicking = False
        
        self.anim_frame += 1
        self.jump_frame += 1

    def punch(self):
        self.punching = True
        self.anim_frame = 0
    
    def kick(self):
        self.kicking = True
        self.anim_frame = 0
    
    def take_damage(self, dmg):
        self.health -= dmg
    
    def left(self):
        self.speed_x -= 15
        if self.looking_right:
            self.looking_right = False
            self.sprite_map.flip()
    
    def right(self):
        self.speed_x += 15
        if not self.looking_right:
            self.looking_right = True
            self.sprite_map.flip()

    def jump(self):
        if self.jump_frame > JUMP_DURATION:
            self.jump_frame = 1
