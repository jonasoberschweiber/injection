import pygame

from fireball import Fireball

class Mutation:
    def __init__(self, s):
        self.image_full = pygame.image.load("gfx/mutations/%s_full.png" % s).convert_alpha()
        self.image_left = pygame.image.load("gfx/mutations/%s_left.png" % s).convert_alpha()
        self.image_right = pygame.image.load("gfx/mutations/%s_right.png" % s).convert_alpha()
        self.image_left_inactive = pygame.image.load("gfx/mutations/%s_left_inactive.png" % s).convert_alpha()
        self.image_right_inactive = pygame.image.load("gfx/mutations/%s_right_inactive.png" % s).convert_alpha()
        self.image_left_disabled = pygame.image.load("gfx/mutations/%s_left_disabled.png" % s).convert_alpha()
        self.image_right_disabled = pygame.image.load("gfx/mutations/%s_right_disabled.png" % s).convert_alpha()
        self.name = s
        
    def activated(self, fighter):
        pass

    def deactivated(self, fighter):
        pass

class SwiftFeetMutation(Mutation):
    DURATION = 200

    def __init__(self):
        Mutation.__init__(self, "swiftfeet")
        self.frame = 0
    
    def swift(self, fighter):
        self.count += 1
        if self.count >= 3:
            return
        fighter.speed_x *= 2
        fighter.speed_reset_l = fighter.speed_x
        fighter.speed_reset_r = fighter.speed_x
        fighter.speed_multi = 2
        self.frame = 0
    
    def deswift(self, fighter):
        fighter.speed_x /= 2
        fighter.speed_reset_l = fighter.speed_x
        fighter.speed_reset_r = fighter.speed_x
        fighter.speed_multi = 1
        self.frame = -1
    
    def update(self):
        if self.frame >= 0:
            self.frame += 1
            if self.frame == self.DURATION:
                self.deswift(self.fighter)


    def activated(self, fighter):
        self.fighter = fighter
        self.frame = -1
        self.count = 0
        fighter.register_key_sequence('rightright', self.swift)
        fighter.register_key_sequence('leftleft', self.swift)
        fighter.update_callbacks.append(self.update)
    
    def deactivated(self, fighter):
        if self.update in fighter.update_callbacks:
            fighter.update_callbacks.remove(self.update)
        fighter.deregister_key_sequence('rightright')
        fighter.deregister_key_sequence('leftleft')
        if self.frame >= 0:
            self.deswift(fighter)

class HundredPercentMoreSpeedMutation(Mutation):
    def __init__(self):
        Mutation.__init__(self, "swiftfeet")

    def activated(self, fighter):
        fighter.speed_multi = 2
    
    def deactivated(self, fighter):
        fighter.speed_multi = 1

class MagicalAffinityMutation(Mutation):
    def __init__(self):
        Mutation.__init__(self, "magicalaffinity")
    
    def fireball(self, fighter):
        fighter.game.fireballs.append(Fireball(fighter.game, fighter))

    def activated(self, fighter):
        fighter.register_key_sequence('rightpunchpunch', self.fireball)
        fighter.register_key_sequence('leftpunchpunch', self.fireball)

    def deactivated(self, fighter):
        fighter.deregister_key_sequence('rightrightpunch')
        fighter.deregister_key_sequence('leftleftpunch')

class HardenedSkinMutation(Mutation):
    def __init__(self):
        Mutation.__init__(self, "hardenedskin")

    def activated(self, fighter):
        fighter.damage_reduction += .4

    def deactivated(self, fighter):
        fighter.damage_reduction -= .4

class WingsMutation(Mutation):
    def __init__(self):
        Mutation.__init__(self, "wings")

    def activated(self, fighter):
        fighter.jump_max = 2

    def deactivated(self, fighter):
        fighter.jump_max = 1

class TranquilityMutation(Mutation):
    LIFE_GAINED = 50
    GAIN_TIME = 160

    def __init__(self):
        Mutation.__init__(self, "tranquility")
    
    def update(self):
        if self.frame % self.GAIN_TIME == 0:
            self.fighter.increase_health(self.LIFE_GAINED)
        self.frame += 1
    
    def damage_veto(self, damage, kind):
        if kind == 'magical':
            return 0
        else:
            return damage

    def activated(self, fighter):
        self.fighter = fighter
        self.frame = 0
        fighter.damage_veto_callbacks.append(self.damage_veto)
        fighter.update_callbacks.append(self.update)
        
    def deactivated(self, fighter):
        if self.damage_veto in fighter.damage_veto_callbacks:
            fighter.damage_veto_callbacks.remove(self.damage_veto)
            fighter.update_callbacks.remove(self.update)

class ToxicMutation(Mutation):
    DAMAGE = 10
    DAMAGE_EVERY = 10
    DAMAGE_FOR = 50

    def __init__(self):
        Mutation.__init__(self, "toxic")

    def opponent_damage_taken(self, health, dmg, kind):
        if not self.opponent_update in self.opponent.update_callbacks and kind == 'physical':
            self.frame = 0
            self.opponent.update_callbacks.append(self.opponent_update)
    
    def opponent_update(self):
        if self.frame == self.DAMAGE_FOR:
            self.opponent.update_callbacks.remove(self.opponent_update)
        if self.frame % self.DAMAGE_EVERY == 0:
            self.opponent.take_damage(self.DAMAGE, 0, 'magical', 1)
        self.frame += 1

    def activated(self, fighter):
        self.fighter = fighter
        self.opponent = fighter.opponent()
        self.opponent.damage_callbacks.append(self.opponent_damage_taken)

    def deactivated(self, fighter):
        if not hasattr(self, 'opponent'):
            return
        if self.opponent_damage_taken in self.opponent.damage_callbacks:
            self.opponent.damage_callbacks.remove(self.opponent_damage_taken)

class StrengthMutation(Mutation):
    def __init__(self):
        Mutation.__init__(self, "strength")

    def activated(self, fighter):
        fighter.damage_modifier += .4

    def deactivated(self, fighter):
        fighter.damage_modifier -= .4
