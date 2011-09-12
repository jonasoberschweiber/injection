import json

import pygame

class World:
    def __init__(self, game, worldfile):
        self.game = game
        self.data = json.loads(open(worldfile).read())
        self.background = pygame.image.load(self.data['bg'])
        self.offset = (0, 0)
        self.platforms = [((x[0], x[1]), (x[2], x[3])) for x in self.data['platforms']]

    def render(self, surface):
        area = self.background.get_rect()
        area.left = self.game.viewport.offset

        surface.blit(self.background, (0, 0), area)

    def obstacles(self, caller):
        obstacles = list(self.platforms)
        opp = self.opponent(caller);
        hb = opp.hit_boxes()
        t = max([x.top for x in hb])
        l = min([x.left for x in hb])
        r = max([x.right for x in hb])
        obstacles.append(((l, t), (r, t)))
        return obstacles

    def contains_point(self, point):
        real_x = point[0] + self.offset[0]
        real_y = point[1] + self.offset[1]

        if real_x > 0 and real_x + 200 < self.background.get_rect().width:
            return True
        return False

    def opponent(self, caller):
        opp = self.game.fighter2
        if opp == caller:
            opp = self.game.fighter1
        return opp

    def hit_opponent(self, caller, damage):
        opp = self.opponent(caller)
        opp_hb = opp.hit_boxes()
        if any([x.collidelist(opp_hb) != -1 for x in caller.hit_boxes()]):
            opp.take_damage(damage)

    def collides_opponent(self, caller, hit_boxes):
        opponent = self.opponent(caller)
        
        opponent_hit_boxes = opponent.hit_boxes()
        a = False
        for b1 in hit_boxes:
            for b2 in opponent_hit_boxes:
                a = (((b1.left >= b2.left and b1.left <= b2.right)
                        or (b1.right >= b2.left and b1.right <= b2.right))
                    and ((b1.top <= b2.bottom and b1.bottom >= b2.top)))
        return a
