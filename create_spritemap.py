import sys
import os
import json
import Image

SPRITES_PER_ROW = 10
SPRITE_WIDTH = 128
SPRITE_HEIGHT = 256

os.chdir('gfx')

sprite_data = json.loads(open(sys.argv[1]).read())

outimage = Image.new('RGBA', ((len(sprite_data['sprites']) % SPRITES_PER_ROW + 1) * SPRITE_WIDTH,
							  (len(sprite_data['sprites']) / SPRITES_PER_ROW + 1) * SPRITE_HEIGHT))

for name, props in sprite_data['sprites'].items():
	x = props['index'] % SPRITES_PER_ROW * SPRITE_WIDTH
	y = props['index'] / SPRITES_PER_ROW * SPRITE_HEIGHT
	sprite_img = Image.open(props['file'])
	outimage.paste(sprite_img, (x, y))

outimage.save(sprite_data['map'], 'PNG')