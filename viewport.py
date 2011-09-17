import pygame

class Viewport:
    def __init__(self, game):
        self.game = game
        self.offset = 0

    def real_rect(self, rect):
        return pygame.Rect(rect.x - self.offset, rect.y, rect.width, rect.height)

    def can_move(self, caller, new_rect):
        opponent = self.game.opponent(caller)
        new_caller_rect = new_rect
        opp_real_rect = self.real_rect(opponent.rect)

        if new_caller_rect.left < 0 or new_caller_rect.right > self.game.world.background.get_rect().width:
            return False

        d = abs(new_caller_rect.x - opponent.rect.x)
        if d >= (1024 - 128):
            if caller.rect.x > opponent.rect.x and caller.speed_x > 0:
                return False
            elif caller.rect.x < opponent.rect.x and caller.speed_x < 0:
                return False

        if self.real_rect(new_caller_rect).left < 0 or self.real_rect(new_caller_rect).right > 1024:
            self.offset += new_caller_rect.x - caller.rect.x
        return True
