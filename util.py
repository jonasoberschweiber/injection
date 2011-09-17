import pygame

def create_colorizer(color):
    def colorize(image):
        return colorize_image(image, color)
    return colorize

def colorize_image(image, color):
    # This is not very efficient, but it works and the only place it gets called
    # is when we load the sprites.
    arr = pygame.PixelArray(image)
    for x in range(0, image.get_width()):
        for y in range(0, image.get_height()):
            if arr[x][y] > 0:
                ratio = max(1, arr[x][y] >> 24) / 255.0
                arr[x][y] = pygame.Color(int(color.r * ratio), int(color.g * ratio), 
                                         int(color.b * ratio), int(color.a * ratio))
    return arr.make_surface()

def collide_line_top(rect, line):
    collide_left = rect.left > line[0][0]
    collide_right = rect.right < line[1][0]
    collide_top = rect.bottom == line[0][1]
    return collide_left and collide_right and collide_top
