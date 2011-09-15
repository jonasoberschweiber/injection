import math
import pygame
import util

from spritemap import SpriteMap
from fireball import Fireball

import mutation

JUMP_SPEED = -100
JUMP_DURATION = 10

KICK_DAMAGE = 45
PUNCH_DAMAGE = 35

PUSHBACK_DISTANCE = 10

SEQUENCE_LIMIT = 40

class Fighter(pygame.sprite.Sprite):
    def __init__(self, game, color, startpos=(0, 0)):
        pygame.sprite.Sprite.__init__(self)
        self.game = game
        self.color = color
        self.sprite_map = SpriteMap('gfx/fighter.json', filter=util.create_colorizer(self.color))
        self.rect = pygame.Rect(startpos[0], startpos[1], 128, 256)
        self.sprite = 'still'
        self.speed_x = 0
        self.speed_y = 0
        self.looking_right = True
        self.wins = 0
        self.start_pos = startpos

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
                           (mutation.WingsMutation(), mutation.SwiftFeetMutation(), None), 
                           (mutation.StrengthMutation(), mutation.ToxicMutation(), None)]
        self.current_injection = 0

        # holds the speed to be subtracted when the user lifts the 'left' or 'right'
        # button
        self.speed_reset_l = 0
        self.speed_reset_r = 0

        # holds pushback amount
        self.pushback = 0

        # used to keep track of whether a keypress belongs to a sequence:
        # when a key is pressed and sequence_frame is smaller than SEQUENCE_LIMIT
        # the key is added to the key sequence
        # if sequence_frame is greater than or equal to SEQUENCE_LIMIT, the key sequence
        # and sequence frame number are reset
        self.sequence_frame = 0
        self.current_sequence = ''
        self.sequence_listeners = {}

        self.switch_to_injection(0)

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

        if not self.pushback:
            new_rect = self.rect.move(self.speed_x - self.pushback, dy)
        else:
            new_rect = self.rect.move(self.speed_x - self.pushback, dy*.35)
            if self.pushback > 0:
                self.pushback -= 1
            elif self.pushback < 0:
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
        self.sequence_frame += 1
        if self.jump_frame > JUMP_DURATION:
            self.jump_count = 0

    def punch(self):
        if self.punching or self.kicking or self.pushback > 0:
            return
        self.register_keypress('punch')
        self.punching = True
        self.anim_frame = 0
        self.punch_sound.play()
    
    def kick(self):
        if self.punching or self.kicking or self.pushback > 0:
            return
        self.register_keypress('kick')
        self.kicking = True
        self.anim_frame = 0
        self.kick_sound.play()
    
    def take_damage(self, dmg, direction, kind='physical'):
        dmg = int((1 - self.damage_reduction) * dmg)
        self.health -= dmg
        for cb in self.damage_callbacks:
            cb(self.health, dmg)
        self.hit_sound.play()
        # we want a little pushback
        self.pushback = PUSHBACK_DISTANCE * direction
        self.game.check_state()
    
    def left(self):
        self.speed_x -= 20 * self.speed_multi
        self.speed_reset_l = -20 * self.speed_multi
        if self.looking_right:
            self.register_keypress('back')
            self.looking_right = False
            self.sprite_map.flip()
        else:
            self.register_keypress('forward')
    
    def right(self):
        self.speed_x += 20 * self.speed_multi
        self.speed_reset_r = 20 * self.speed_multi
        if not self.looking_right:
            self.register_keypress('back')
            self.looking_right = True
            self.sprite_map.flip()
        else:
            self.register_keypress('forward')

    def stop_left(self):
        self.speed_x -= self.speed_reset_l

    def stop_right(self):
        self.speed_x -= self.speed_reset_r

    def jump(self):
        if self.jump_count < self.jump_max:
            self.jump_count += 1
            self.jump_frame = 1
    
    def opponent(self):
        return self.game.opponent(self)

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
    
    def reset(self):
        self.health = 1000
        self.speed_x = 0
        self.speed_reset_l = 0
        self.speed_reset_r = 0
        self.rect.left = self.start_pos[0]
        self.rect.top = self.start_pos[1]
        self.switch_to_injection(0)
        if self.rect.left < self.game.opponent(self).rect.left:
            if not self.looking_right:
                self.sprite_map.flip()
                self.looking_right = True
        else:
            if self.looking_right:
                self.sprite_map.flip()
                self.looking_right = False

    def register_keypress(self, key):
        if self.sequence_frame < SEQUENCE_LIMIT:
            self.current_sequence += key
            if self.sequence_listeners.has_key(self.current_sequence):
                self.sequence_listeners[self.current_sequence](self)
        else:
            self.sequence_frame = 0
            self.current_sequence = key
    
    def register_key_sequence(self, sequence, listener):
        self.sequence_listeners[sequence] = listener
    
    def deregister_key_sequence(self, sequence):
        if self.sequence_listeners.has_key(sequence):
            self.sequence_listeners.pop(sequence)

