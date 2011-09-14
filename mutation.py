import pygame

class Mutation:
    def __init__(self, s):
        self.image_full = pygame.image.load("gfx/mutations/%s_full.png" % s)
        self.image_left = pygame.image.load("gfx/mutations/%s_left.png" % s)
        self.image_right = pygame.image.load("gfx/mutations/%s_right.png" % s)
        self.image_left_inactive = pygame.image.load("gfx/mutations/%s_left_inactive.png" % s)
        self.image_right_inactive = pygame.image.load("gfx/mutations/%s_right_inactive.png" % s)
        self.image_left_disabled = pygame.image.load("gfx/mutations/%s_left_disabled.png" % s)
        self.image_right_disabled = pygame.image.load("gfx/mutations/%s_right_disabled.png" % s)
        
    def activated(self, fighter):
        pass

    def deactivated(self, fighter):
        pass

class SwiftFeetMutation(Mutation):
    def __init__(self):
        Mutation.__init__(self, "swiftfeet")

    def activated(self, fighter):
        fighter.speed_x *= 2
        fighter.speed_reset_l = fighter.speed_x
        fighter.speed_reset_r = fighter.speed_x
        fighter.speed_multi = 2
    
    def deactivated(self, fighter):
        fighter.speed_x /= 2
        fighter.speed_reset_l = fighter.speed_x
        fighter.speed_reset_r = fighter.speed_x
        fighter.speed_multi = 1

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

    def activated(self, fighter):
        pass

    def deactivated(self, fighter):
        pass

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
        pass

    def deactivated(self, fighter):
        pass

class TranquilityMutation(Mutation):
    def __init__(self):
        Mutation.__init__(self, "tranquility")

    def activated(self, fighter):
        pass
        
    def deactivated(self, fighter):
        pass

class ToxicMutation(Mutation):
    def __init__(self):
        Mutation.__init__(self, "toxic")

    def activated(self, fighter):
        pass

    def deactivated(self, fighter):
        pass

class StrengthMutation(Mutation):
    def __init__(self):
        Mutation.__init__(self, "strength")

    def activated(self, fighter):
        fighter.damage_modifier += .4

    def deactivated(self, fighter):
        fighter.damage_modifier -= .4
