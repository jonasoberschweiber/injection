import pygame 

class RoundCounter:
    def __init__(self, game, rect):
        self.game = game
        self.rounds = (pygame.image.load("gfx/round1.png").convert_alpha(),
                       pygame.image.load("gfx/round2.png").convert_alpha(), 
                       pygame.image.load("gfx/round3.png").convert_alpha())
        self.img_ready = pygame.image.load("gfx/ready.png").convert_alpha()
        self.img_go = pygame.image.load("gfx/go.png").convert_alpha()
        self.snd_newround = pygame.mixer.Sound("snd/new_round.wav")
        self.round = -1
        self.rect = rect
        self.animation_frame = 0

        self.img_wins = pygame.image.load("gfx/wins.png").convert_alpha()
        self.img_win_circle = pygame.image.load("gfx/win_circle.png").convert_alpha()
        self.win_color = pygame.Color(200, 20, 20)
        self.wins_rect1 = pygame.Rect(295, 58, 0, 0)
        self.wins_rect2 = pygame.Rect(958, 58, 0, 0)

    def render(self, surface):
        n = self.round
        if self.round > len(self.rounds) - 1:
            n = 0
        surface.blit(self.rounds[n], self.rect)
        surface.blit(self.img_wins, self.wins_rect1)
        surface.blit(self.img_wins, self.wins_rect2)
        for i in range(0, self.game.fighter1.wins):
            #pygame.draw.circle(surface, self.win_color, (self.wins_rect1.left + i*20, self.wins_rect1.top + 20), 4)
            surface.blit(self.img_win_circle, (self.wins_rect1.left + i*12, self.wins_rect1.top + 13))
        for i in range(0, self.game.fighter2.wins):
            #pygame.draw.circle(surface, self.win_color, (self.wins_rect2.left + i*20, self.wins_rect2.top + 20), 4)
            surface.blit(self.img_win_circle, (self.wins_rect2.left + i*12, self.wins_rect2.top + 13))

        if self.animation_frame > 0:
            if self.animation_frame < 50:
                if self.animation_frame == 1:
                    pygame.mixer.music.stop()
                    pygame.mixer.music.rewind()
                elif self.animation_frame == 25:
                    self.snd_newround.play()
            elif self.animation_frame < 105:
                surface.blit(self.img_ready, (345, 261))
            elif self.animation_frame < 115:
                surface.blit(self.img_ready, (345, 261))
                surface.blit(self.img_go, (540, 261))
                self.game.ignore_keys = False
                if self.animation_frame == 105:
                    pygame.mixer.music.play()
            else:
                self.animation_frame = 0
                return
            self.animation_frame += 1

    def next_round(self):
        self.game.ignore_keys = True
        self.round += 1
        self.animation_frame = 1

    def reset(self):
        self.round = 0
