import pygame

def create_colorizer(color):
	def colorize(image):
		return colorize_image(image, color)
	return colorize

def colorize_image(image, color):
    arr = pygame.PixelArray(image)
    arr.replace(pygame.Color(0, 0, 0, 255), color, distance=0.9)
    return arr.make_surface()
