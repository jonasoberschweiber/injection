import math
import pygame
import util

from spritemap import SpriteMap

import mutation

JUMP_SPEED = -100
JUMP_DURATION = 15

KICK_DAMAGE = 10
PUNCH_DAMAGE = 5

class Fighter(pygame.sprite.Sprite):
    def __init__(self, game, color):
        pygame.sprite.Sprite.__init__(self)
        self.game = game
        self.color = color
        self.sprite_map = SpriteMap('gfx/fighter.json', filter=util.create_colorizer(self.color))
        self.rect = pygame.Rect(0, 0, 128, 256)
        self.sprite = 'still'
        self.speed_x = 0
        self.speed_y = 0
        self.looking_right = True

        # speed multiplicator
        self.speed_multi = 1
        self.health = 100
        self.punching = False
        self.kicking = False
        self.anim_frame = 0
        self.jump_frame = 0
        self.damage_callbacks = []
        self.injection_callbacks = []

        self.injections = [(mutation.FiftyPercentMoreSpeedMutation(), mutation.HundredPercentMoreSpeedMutation(), None),
                           (mutation.HundredPercentMoreSpeedMutation(), mutation.MagicalAffinityMutation(), None)]
        self.current_injection = 0

        # holds the speed to be subtracted when the user lifts the 'left' or 'right'
        # button
        self.speed_reset_l = 0
        self.speed_reset_r = 0

        # holds pushback amount
        self.pushback = 0

    def render(self, surface):
        off = self.sprite_map.offset(self.sprite)
        rect = self.game.viewport.real_rect(self.rect)
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
        for platform in self.game.world.obstacles(self):
            if not util.collide_line_top(self.rect, platform):
                if self.rect.right > platform[0][0] and self.rect.left < platform[1][0]:
                    dy = min(dy, abs(self.rect.bottom - platform[0][1]))
            else:
                dy = 0
        dy += math.trunc(JUMP_SPEED * math.cos((math.pi / (2 * JUMP_DURATION)) * min(self.jump_frame, JUMP_DURATION)))
        new_rect = self.rect.move(self.speed_x - self.pushback, dy)
        if self.pushback != 0:
            self.pushback = 0

        if not self.game.viewport.can_move(self, new_rect):
            new_rect.left = self.rect.left
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
                self.game.hit_opponent(self, PUNCH_DAMAGE)
            elif self.anim_frame >= 6:
                self.sprite = 'still'
                self.punching = False

        if self.kicking:
            if self.anim_frame == 0:
                self.sprite = 'kick02'
            elif self.anim_frame == 3:
                self.sprite = 'kick03'
                self.game.hit_opponent(self, KICK_DAMAGE)
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
    
    def take_damage(self, dmg, direction):
        self.health -= dmg
        for cb in self.damage_callbacks:
            cb(self.health)
        # we want a little pushback
        self.pushback = 15 * direction
    
    def left(self):
        self.speed_x -= 15 * self.speed_multi
        self.speed_reset_l = -15 * self.speed_multi
        if self.looking_right:
            self.looking_right = False
            self.sprite_map.flip()
    
    def right(self):
        self.speed_x += 15 * self.speed_multi
        self.speed_reset_r = 15 * self.speed_multi
        if not self.looking_right:
            self.looking_right = True
            self.sprite_map.flip()

    def stop_left(self):
        self.speed_x -= self.speed_reset_l

    def stop_right(self):
        self.speed_x -= self.speed_reset_r

    def jump(self):
        if self.jump_frame > JUMP_DURATION:
            self.jump_frame = 1

    def switch_to_injection(self, number):
        for m in self.injections[self.current_injection]:
            if m != None:
                m.deactivated(self)
        for m in self.injections[number]:
            if m != None:
                m.activated(self)
        self.current_injection = number
        for cb in self.injection_callbacks:
            cb(number)
