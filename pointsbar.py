import pygame

class PointsBar:
	def __init__(self, fighter, rect):
		fighter.damage_callbacks.append(self.damage_taken)
		self.fighter = fighter
		self.rect = rect

	def damage_taken(self, new_health):
		pass

	def render(self, surface):
		pygame.draw.rect(surface, pygame.Color(0, 0, 0, 255), self.rect, width=5)
