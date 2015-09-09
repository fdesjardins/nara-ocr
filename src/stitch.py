import os, sys, math
import Image

from utils import *

OUT_COLUMNS = 80
COL_WIDTH = 75
ROW_HEIGHT = 75
OUT_FORMAT = 'png'
			
def main():
	
	input_images = []
	input_images2 = []
	
	infile = sys.argv[1]
	
	#check that the initial file is valid
	try:
		im = Image.open(infile)
		print infile, im.format, "%dx%d" % im.size, im.mode

	except IOError:
		print 'Invalid input image.'
		return
	
	#filename prefix and extension
	prefix = infile[:-5]
	extension = infile[-4:]
	
	ix = 0
	#Load all input images into input_images
	print '\nLoading images into memory',
	while(1):
		try:
			im = Image.open(prefix + str(ix) + extension)
			print prefix + str(ix) + extension
			background = Image.new('RGB', im.size, (255, 255, 255))
			background.paste(im)
			input_images.append(background)
			ix += 1
		except IOError:
			break
			
	print 'Count: ' + str(ix)
	
	max_w, max_h = max_size(input_images)
	
	print '\nMaxW: ' + str(max_w),
	print 'MaxH: ' + str(max_h) + '\n'
		
	if len(input_images) > OUT_COLUMNS: 
		col = OUT_COLUMNS
	else:
		col = len(input_images)
		
	#strictly vertical stitching
	try:
		vert = sys.argv[2]
	except:
		vert = '0'
		
	if vert == '-v':
	
		#create a background to place all of our images on
		bg_width, bg_height = max_w, len(input_images) * max_h
		print 'Output Width: ' + str(bg_width), 
		print 'Output Heigth: ' + str(bg_height)
		background = Image.new('RGB', (bg_width, bg_height), (255, 255, 255))
		
		top_margin = 0
		#paste the images into the background
		for i, img in enumerate(input_images):
			background.paste(img, (0, top_margin))
			top_margin += max_h

	#regular columnar stitching
	else:
	
		#create a background to place all of our images on
		bg_width, bg_height = col*max_w, int( math.ceil( len(input_images)/float(OUT_COLUMNS) ) * max_h)
		print 'Output Width: ' + str(bg_width), 
		print 'Output Heigth: ' + str(bg_height)
		background = Image.new('RGB', (bg_width, bg_height), (255, 255, 255))
		
		left_margin, top_margin = 0, 0
		#paste the images into the background at correct spacing
		for i, img in enumerate(input_images):
			
			background.paste(img, (left_margin, top_margin))
			
			#if at end of current line, start a newline
			if i%OUT_COLUMNS == 0 and i != 0:
				top_margin += max_h
				left_margin = 0
			else:
				left_margin += max_w
			
	background.save(prefix + 'all.' + OUT_FORMAT, OUT_FORMAT)
	
if __name__=='__main__':
	main()