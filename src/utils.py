import sys, os
import Image, ImageMath

def flatten(lst):
	"Recursively flattens a nested list"
	return sum( ([x] if not isinstance(x, list) else flatten(x)
			 for x in lst), [] )

def gen_directories(prefix='char_'):
	'''Creates the directory structure used for the dict_stitch procedure'''
	
	#only using uppercase for now
	#lc_alphabet = map(chr, range(97, 123))
	uc_alphabet = map(chr, range(65, 91))
	numbers = map(str, range(0, 10))
	
	alphanumeric = uc_alphabet + numbers	#+ lc_alphabet
	
	for ch in alphanumeric:
		dir = prefix + ch
		if not os.path.exists(dir):
			os.makedirs(dir)

def max_size(input_images):
	'''Returns the max width, max height of every image in input_images'''

	max_width, max_height = 0, 0
	#find max width, height in input_data
	for img in input_images:
		new_width, new_height = img.size
		if new_width > max_width:
			max_width = new_width
		if new_height > max_height:
			max_height = new_height
			
	return max_width, max_height
