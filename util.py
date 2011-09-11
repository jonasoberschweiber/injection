import pygame

def create_colorizer(color):
	def colorize(image):
		return colorize_image(image, color)
	return colorize

def colorize_image(image, color):
    arr = pygame.PixelArray(image)
    arr.replace(pygame.Color(0, 0, 0, 255), color, distance=0.9)
    return arr.make_surface()

def collide_line_top(rect, line):
    collide_left = rect.left > line[0][0]
    collide_right = rect.right < line[1][0]
    collide_top = rect.bottom == line[0][1]
    return collide_left and collide_right and collide_top
