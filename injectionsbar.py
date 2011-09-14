import pygame

class Injection:
    def __init__(self, mutations, rect, active=0):
        self.mutations = mutations
        self.rect = rect
        self.separator = pygame.image.load("gfx/mutation_separator.png")
        self.separator_trans = pygame.image.load("gfx/mutation_separator_trans.png")
        self.active = active

    def render(self, surface):
        if self.active:
            surface.blit(self.mutations[0].image_left, self.rect)
            surface.blit(self.separator, self.rect.move(31, 0))
            surface.blit(self.mutations[1].image_right, self.rect.move(32, 0))
        else:
            surface.blit(self.mutations[0].image_left_inactive, self.rect)
            surface.blit(self.separator_trans, self.rect.move(31, 0))
            surface.blit(self.mutations[1].image_right_inactive, self.rect.move(32, 0))

class InjectionsBar:
    def __init__(self, fighter, rect):
        fighter.injection_callbacks.append(self.injections_switched)
        self.fighter = fighter
        self.rect = rect
        self.injections = []

        r = pygame.Rect(self.rect.left, self.rect.top, 62, 32)
        for i in range(0, len(self.fighter.injections)):
            if i == self.fighter.current_injection:
                inj = Injection(self.fighter.injections[i], r, 1)
            else:
                inj = Injection(self.fighter.injections[i], r)
            self.injections.append(inj)
            r = r.move(67, 0)

    def injections_switched(self, new_injection):
        for i in range(0, len(self.injections)):
            if i == new_injection:
                self.injections[i].active = True
            else:
                self.injections[i].active = False

    def render(self, surface):
        for injection in self.injections:
            injection.render(surface)
