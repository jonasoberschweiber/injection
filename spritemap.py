import json
import pygame

SPRITES_PER_ROW = 10

class SpriteMap:
	def __init__(self, property_file, width=128, height=256, filter=None):
		self.width = width
		self.height = height
		self.flipped = False
		self.properties = json.loads(open(property_file).read()) 
		if filter != None:
			self.map = filter(pygame.image.load(self.properties['map']).convert_alpha())
		else:
			self.map = pygame.image.load(self.properties['map']).convert_alpha()
		self.build_flipped_map()
		self.build_masks()

	def build_masks(self):
		self.masks = {}
		self.flipped_masks = {}
		for name in self.properties['sprites']:
			self.masks[name] = pygame.mask.from_surface(self.map.subsurface(self.sprite_rect(name)), 200)
			self.flipped_masks[name] = pygame.mask.from_surface(self.flipped_map.subsurface(self.sprite_rect(name)))
	
	def build_flipped_map(self):
		self.flipped_map = pygame.Surface((self.map.get_width(), self.map.get_height()), flags=self.map.get_flags(),
			depth=self.map.get_bitsize())
		for name in self.properties['sprites']:
			rect = self.sprite_rect(name)
			sprite = self.map.subsurface(rect)
			flipped = pygame.transform.flip(sprite, True, False)
			self.flipped_map.blit(flipped, rect)


	def sprite_rect(self, name):
		sprite = self.properties['sprites'][name]
		x = sprite['index'] % SPRITES_PER_ROW * self.width
		y = sprite['index'] / SPRITES_PER_ROW * self.height
		width = self.width
		if sprite.has_key('oversize') and sprite['oversize']:
			width += self.width
		return (x, y, width, self.height)

	def image(self):
		if self.flipped:
			return self.flipped_map
		else:
			return self.map

	def offset(self, name):
		sprite = self.properties['sprites'][name]
		if sprite.has_key('offset'):
			if self.flipped:
				return self.width - sprite['offset']
			return sprite['offset'] 
		return 0
	
	def mask(self, name):
		return self.masks[name]
	
	def flip(self):
		self.flipped = not self.flipped
