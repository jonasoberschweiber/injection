import json
import pygame

SPRITES_PER_ROW = 10

class SpriteMap:
	def __init__(self, property_file, width=128, height=256):
		self.width = width
		self.height = height
		self.properties = json.loads(open(property_file).read()) 
		self.map = pygame.image.load(self.properties['map'])

	def sprite_coords(self, name):
		sprite = self.properties['sprites'][name]
		x = sprite['index'] % SPRITES_PER_ROW * self.width
		y = sprite['index'] / SPRITES_PER_ROW * self.height
		return (x, y)
