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
        obstacles = self.platforms
        return obstacles

    def contains_point(self, point):
        real_x = point[0] + self.offset[0]
        real_y = point[1] + self.offset[1]

        if real_x > 0 and real_x + 200 < self.background.get_rect().width:
            return True
        return False


    def collides_opponent(self, caller, hit_boxes):
        opponent = self.game.opponent(caller)
        
        opponent_hit_boxes = opponent.hit_boxes()
        a = False
        for b1 in hit_boxes:
            for b2 in opponent_hit_boxes:
                a = (((b1.left >= b2.left and b1.left <= b2.right)
                        or (b1.right >= b2.left and b1.right <= b2.right))
                    and ((b1.top <= b2.bottom and b1.bottom >= b2.top)))
        return a
