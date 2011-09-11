import pygame

class World:
    def __init__(self, bgfile):
        self.background = pygame.image.load(bgfile)
        self.offset = (0, 0)
        self.platforms = [((0, 675), (1000, 660))]
        self.fighter1 = ""
        self.fighter2 = ""

    def render(self, surface):
        area = self.background.get_rect()
        area.left = self.offset[0]
        area.top = self.offset[1]

        surface.blit(self.background, (0, 0), area)


    def scroll(self, pixels):
        if (self.fighter1.rect.left - pixels < 0 or self.fighter1.rect.right - pixels > 1024)\
           or (self.fighter2.rect.left - pixels < 0 or self.fighter2.rect.right - pixels > 1024):
            return False
        self.offset = (self.offset[0] + pixels, self.offset[1])
        self.fighter1.rect.left -= pixels
        self.fighter2.rect.left -= pixels
        return True

    def contains_point(self, point):
        real_x = point[0] + self.offset[0]
        real_y = point[1] + self.offset[1]

        if real_x > 0 and real_x + 200 < self.background.get_rect().width:
            return True
        return False

    def collides_opponent(self, caller, hit_boxes):
        opponent = self.fighter2
        if opponent == caller:
            opponent = self.fighter1
        
        opponent_hit_boxes = opponent.hit_boxes()
        return any([x.collidelist(opponent_hit_boxes) != -1 for x in hit_boxes])