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
