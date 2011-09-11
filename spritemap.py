import json
import pygame

SPRITES_PER_ROW = 10

class SpriteMap:
	def __init__(self, property_file, width=128, height=256, filter=None):
		self.width = width
		self.height = height
		self.properties = json.loads(open(property_file).read()) 
		if filter != None:
			self.map = filter(pygame.image.load(self.properties['map']))
		else:
			self.map = pygame.image.load(self.properties['map'])

	def sprite_rect(self, name):
		sprite = self.properties['sprites'][name]
		x = sprite['index'] % SPRITES_PER_ROW * self.width
		y = sprite['index'] / SPRITES_PER_ROW * self.height
		width = self.width
		if sprite.has_key('oversize') and sprite['oversize']:
			width += self.width
		return (x, y, width, self.height)

	def image(self):
		return self.map

	def offset(self, name):
		sprite = self.properties['sprites'][name]
		if sprite.has_key('offset'):
			return sprite['offset']
		return 0