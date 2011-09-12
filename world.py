import json

import pygame

class World:
    def __init__(self, worldfile):
        self.data = json.loads(open(worldfile).read())
        self.background = pygame.image.load(self.data['bg'])
        self.offset = (0, 0)
        self.platforms = [((x[0], x[1]), (x[2], x[3])) for x in self.data['platforms']]
        self.fighter1 = ""
        self.fighter2 = ""

    def render(self, surface):
        area = self.background.get_rect()
        area.left = self.offset[0]
        area.top = self.offset[1]

        surface.blit(self.background, (0, 0), area)

    def adjusted_platforms(self):
        pass

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

    def opponent(self, caller):
        opp = self.fighter2
        if opp == caller:
            opp = self.fighter1
        return opp

    def hit_opponent(self, caller, damage):
        opp = self.opponent(caller)
        opp_hb = opp.hit_boxes()
        if any([x.collidelist(opp_hb) != -1 for x in caller.hit_boxes()]):
            opp.take_damage(damage)

    def collides_opponent(self, caller, hit_boxes):
        opponent = self.opponent(caller)
        
        opponent_hit_boxes = opponent.hit_boxes()
        return any([x.collidelist(opponent_hit_boxes) != -1 for x in hit_boxes])