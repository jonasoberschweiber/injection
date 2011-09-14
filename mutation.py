import pygame

class Mutation:
    def activated(self, fighter):
        pass

    def deactivated(self, fighter):
        pass

class FiftyPercentMoreSpeedMutation(Mutation):
    def __init__(self):
        self.image_full = pygame.image.load("gfx/mutations/swiftfeet_full.png")
        self.image_left = pygame.image.load("gfx/mutations/swiftfeet_left.png")
        self.image_right = pygame.image.load("gfx/mutations/swiftfeet_right.png")
        self.image_left_inactive = pygame.image.load("gfx/mutations/swiftfeet_left_inactive.png")
        self.image_right_inactive = pygame.image.load("gfx/mutations/swiftfeet_right_inactive.png")
        self.image_left_disabled = pygame.image.load("gfx/mutations/swiftfeet_left_disabled.png")
        self.image_right_disabled = pygame.image.load("gfx/mutations/swiftfeet_right_disabled.png")

    def activated(self, fighter):
        fighter.speed_multi = 1.5
    
    def deactived(self, fighter):
        fighter.speed_multi = 1

class HundredPercentMoreSpeedMutation(Mutation):
    def __init__(self):
        self.image_full = pygame.image.load("gfx/mutations/swiftfeet_full.png")
        self.image_left = pygame.image.load("gfx/mutations/swiftfeet_left.png")
        self.image_right = pygame.image.load("gfx/mutations/swiftfeet_right.png")
        self.image_left_inactive = pygame.image.load("gfx/mutations/swiftfeet_left_inactive.png")
        self.image_right_inactive = pygame.image.load("gfx/mutations/swiftfeet_right_inactive.png")
        self.image_left_disabled = pygame.image.load("gfx/mutations/swiftfeet_left_disabled.png")
        self.image_right_disabled = pygame.image.load("gfx/mutations/swiftfeet_right_disabled.png")

    def activated(self, fighter):
        fighter.speed_multi = 2
    
    def deactivated(self, fighter):
        fighter.speed_multi = 1

class MagicalAffinityMutation(Mutation):
    def __init__(self):
        self.image_full = pygame.image.load("gfx/mutations/magicalaffinity_full.png")
        self.image_left = pygame.image.load("gfx/mutations/magicalaffinity_left.png")
        self.image_right = pygame.image.load("gfx/mutations/magicalaffinity_right.png")
        self.image_left_inactive = pygame.image.load("gfx/mutations/magicalaffinity_left_inactive.png")
        self.image_right_inactive = pygame.image.load("gfx/mutations/magicalaffinity_right_inactive.png")
        self.image_left_disabled = pygame.image.load("gfx/mutations/magicalaffinity_left_disabled.png")
        self.image_right_disabled = pygame.image.load("gfx/mutations/magicalaffinity_right_disabled.png")

    def activated(self, fighter):
        pass

    def deactivated(self, fighter):
        pass

class HardenedSkinMutation(Mutation):
    def __init__(self):
        self.image_full = pygame.image.load("gfx/mutations/hardenedskin_full.png")
        self.image_left = pygame.image.load("gfx/mutations/hardenedskin_left.png")
        self.image_right = pygame.image.load("gfx/mutations/hardenedskin_right.png")
        self.image_left_inactive = pygame.image.load("gfx/mutations/hardenedskin_left_inactive.png")
        self.image_right_inactive = pygame.image.load("gfx/mutations/hardenedskin_right_inactive.png")
        self.image_left_disabled = pygame.image.load("gfx/mutations/hardenedskin_left_disabled.png")
        self.image_right_disabled = pygame.image.load("gfx/mutations/hardenedskin_right_disabled.png")

    def activated(self, fighter):
        pass

    def deactivated(self, fighter):
        pass

class WingsMutation(Mutation):
    def __init__(self):
        self.image_full = pygame.image.load("gfx/mutations/wings_full.png")
        self.image_left = pygame.image.load("gfx/mutations/wings_left.png")
        self.image_right = pygame.image.load("gfx/mutations/wings_right.png")
        self.image_left_inactive = pygame.image.load("gfx/mutations/wings_left_inactive.png")
        self.image_right_inactive = pygame.image.load("gfx/mutations/wings_right_inactive.png")
        self.image_left_disabled = pygame.image.load("gfx/mutations/wings_left_disabled.png")
        self.image_right_disabled = pygame.image.load("gfx/mutations/wings_right_disabled.png")

    def activated(self, fighter):
        pass

    def deactivated(self, fighter):
        pass

class TranquilityMutation(Mutation):
    def __init__(self):
        self.image_full = pygame.image.load("gfx/mutations/tranquility_full.png")
        self.image_left = pygame.image.load("gfx/mutations/tranquility_left.png")
        self.image_right = pygame.image.load("gfx/mutations/tranquility_right.png")
        self.image_left_inactive = pygame.image.load("gfx/mutations/tranquility_left_inactive.png")
        self.image_right_inactive = pygame.image.load("gfx/mutations/tranquility_right_inactive.png")
        self.image_left_disabled = pygame.image.load("gfx/mutations/tranquility_left_disabled.png")
        self.image_right_disabled = pygame.image.load("gfx/mutations/tranquility_right_disabled.png")

    def activated(self, fighter):
        pass
        
    def deactivated(self, fighter):
        pass

class ToxicMutation(Mutation):
    def __init__(self):
        self.image_full = pygame.image.load("gfx/mutations/toxic_full.png")
        self.image_left = pygame.image.load("gfx/mutations/toxic_left.png")
        self.image_right = pygame.image.load("gfx/mutations/toxic_right.png")
        self.image_left_inactive = pygame.image.load("gfx/mutations/toxic_left_inactive.png")
        self.image_right_inactive = pygame.image.load("gfx/mutations/toxic_right_inactive.png")
        self.image_left_disabled = pygame.image.load("gfx/mutations/toxic_left_disabled.png")
        self.image_right_disabled = pygame.image.load("gfx/mutations/toxic_right_disabled.png")

    def activated(self, fighter):
        pass

    def deactivated(self, fighter):
        pass

class StrengthMutation(Mutation):
    def __init__(self):
        self.image_full = pygame.image.load("gfx/mutations/strength_full.png")
        self.image_left = pygame.image.load("gfx/mutations/strength_left.png")
        self.image_right = pygame.image.load("gfx/mutations/strength_right.png")
        self.image_left_inactive = pygame.image.load("gfx/mutations/strength_left_inactive.png")
        self.image_right_inactive = pygame.image.load("gfx/mutations/strength_right_inactive.png")
        self.image_left_disabled = pygame.image.load("gfx/mutations/strength_left_disabled.png")
        self.image_right_disabled = pygame.image.load("gfx/mutations/strength_right_disabled.png")

    def activated(self, fighter):
        pass

    def deactivated(self, fighter):
        pass
