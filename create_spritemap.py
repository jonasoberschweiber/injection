import sys
import os
import json
import Image

SPRITES_PER_ROW = 10
SPRITE_WIDTH = 128
SPRITE_HEIGHT = 256

sprite_data = json.loads(open(sys.argv[1]).read())

outimage_r = Image.new('RGBA', ((len(sprite_data['sprites']) % SPRITES_PER_ROW + 1) * SPRITE_WIDTH,
							   (len(sprite_data['sprites']) / SPRITES_PER_ROW + 1) * SPRITE_HEIGHT))
outimage_g = Image.new('RGBA', ((len(sprite_data['sprites']) % SPRITES_PER_ROW + 1) * SPRITE_WIDTH,
                               (len(sprite_data['sprites']) / SPRITES_PER_ROW + 1) * SPRITE_HEIGHT))

clr_g = (0, 0, 200, 255)
clr_r = (200, 0, 0, 255)

for name, props in sprite_data['sprites'].items():
    x = props['index'] % SPRITES_PER_ROW * SPRITE_WIDTH
    y = props['index'] / SPRITES_PER_ROW * SPRITE_HEIGHT
    sprite_img = Image.open(props['file'])
    sprite_img_r = Image.new('RGBA', sprite_img.size)
    sprite_img_g = Image.new('RGBA', sprite_img.size)
    y += SPRITE_HEIGHT - sprite_img.size[1]
    data = sprite_img.getdata()
    for px in range(0, sprite_img.size[0]):
        for py in range(0, sprite_img.size[1]):
            pixel = sprite_img.getpixel((px, py))
            ratio = max(1, pixel[3]) / 255.0
            sprite_img_r.putpixel((px, py), (clr_r[0] * ratio, clr_r[1] * ratio, clr_r[2] * ratio, clr_r[3] * ratio))
            sprite_img_g.putpixel((px, py), (clr_g[0] * ratio, clr_g[1] * ratio, clr_g[2] * ratio, clr_g[3] * ratio))
    outimage_r.paste(sprite_img_r, (x, y))
    outimage_g.paste(sprite_img_g, (x, y))

outimage_g.save(sprite_data['map'] + '_g.png', 'PNG')
outimage_r.save(sprite_data['map'] + '_r.png', 'PNG')