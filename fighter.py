import math
import pygame
import util

from spritemap import SpriteMap

import mutation

JUMP_SPEED = -100
JUMP_DURATION = 10

KICK_DAMAGE = 45
PUNCH_DAMAGE = 35

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

        self.kick_sound = pygame.mixer.Sound('snd/kick_empty.wav')
        self.punch_sound = pygame.mixer.Sound('snd/punch_empty.wav')
        self.hit_sound = pygame.mixer.Sound('snd/kick_hit.wav')

        # speed multiplicator
        self.speed_multi = 1
        self.damage_reduction = 0
        self.damage_modifier = 1
        self.health = 1000
        self.punching = False
        self.kicking = False
        self.anim_frame = 0
        self.jump_frame = 0
        self.jump_count = 0
        self.jump_max = 1
        self.damage_callbacks = []
        self.injection_callbacks = []

        self.injections = [(mutation.MagicalAffinityMutation(), mutation.HardenedSkinMutation(), None),
                           (mutation.WingsMutation(), mutation.HardenedSkinMutation(), None), 
                           (mutation.StrengthMutation(), mutation.ToxicMutation(), None)]
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

    def real_rect(self):
        return self.game.viewport.real_rect(self.rect)

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
                self.game.hit_opponent(self, PUNCH_DAMAGE * self.damage_modifier)
            elif self.anim_frame >= 6:
                self.sprite = 'still'
                self.punching = False

        if self.kicking:
            if self.anim_frame == 0:
                self.sprite = 'kick02'
            elif self.anim_frame == 3:
                self.sprite = 'kick03'
                self.game.hit_opponent(self, KICK_DAMAGE * self.damage_modifier)
            elif self.anim_frame >= 8:
                self.sprite = 'still'
                self.kicking = False
        
        self.anim_frame += 1
        self.jump_frame += 1
        if self.jump_frame > JUMP_DURATION:
            self.jump_count = 0

    def punch(self):
        self.punching = True
        self.anim_frame = 0
        self.punch_sound.play()
    
    def kick(self):
        self.kicking = True
        self.anim_frame = 0
        self.kick_sound.play()
    
    def take_damage(self, dmg, direction):
        dmg = int((1 - self.damage_reduction) * dmg)
        self.health -= dmg
        for cb in self.damage_callbacks:
            cb(self.health, dmg)
        self.hit_sound.play()
        # we want a little pushback
        self.pushback = 15 * direction
    
    def left(self):
        self.speed_x -= 20 * self.speed_multi
        self.speed_reset_l = -20 * self.speed_multi
        if self.looking_right:
            self.looking_right = False
            self.sprite_map.flip()
    
    def right(self):
        self.speed_x += 20 * self.speed_multi
        self.speed_reset_r = 20 * self.speed_multi
        if not self.looking_right:
            self.looking_right = True
            self.sprite_map.flip()

    def stop_left(self):
        self.speed_x -= self.speed_reset_l

    def stop_right(self):
        self.speed_x -= self.speed_reset_r

    def jump(self):
        if self.jump_count < self.jump_max:
            self.jump_count += 1
            self.jump_frame = 1

    def switch_to_injection(self, number):
        for m in self.injections[self.current_injection]:
            if m != None:
                m.deactivated(self)
        for m in self.injections[number]:
            if m != None:
                m.activated(self)
        for cb in self.injection_callbacks:
            cb(self.current_injection, number)
        self.current_injection = number
