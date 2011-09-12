import pygame

class PointsBar:
	def __init__(self, fighter, rect, color):
		fighter.damage_callbacks.append(self.damage_taken)
		self.fighter = fighter
		self.rect = rect
		self.health = 100
		self.color = color

	def damage_taken(self, new_health):
		self.health = new_health

	def render(self, surface):
		pygame.draw.rect(surface, self.color, self.rect, 5)
		r = pygame.Rect(self.rect.x, self.rect.y, self.rect.width/100.0 * self.health, self.rect.height)
		surface.fill(self.color, r)
