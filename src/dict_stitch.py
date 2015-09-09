import os, sys, math, random
import Image

from utils import *

OUT_COLUMNS = 300
OUT_FORMAT = 'png'
FOLDER_PREFIX = 'char_'

# Designates left and top margins. Units are in terms of the maximum width and
# height of the images loaded into memory for the stitching operation. A margin of 2
# will result in a margin of size 2*max_width on each side, and 2*max_height on the top
# and bottom.
MARGIN = 2

def flatten(lst):
	"Recursively flattens a nested list"
	return sum( ([x] if not isinstance(x, list) else flatten(x)
			 for x in lst), [] )
			 
def main(argv):
	
	in_words = []
	indiv_images = []
	
	## open wordlist file
	try:
		f = open(argv[0], 'r')
	except: 
		print 'Invalid input file'
		return
	
	all_words = flatten(map(lambda l: l.split(" "), f.readlines())) # get all words from file
	
	all_words = [word.rstrip() for word in all_words] # remove trailing \n
	
	## grabs the images out of one the char_ folders matching the letter of
	## each word being read. 
	for word in all_words:
		print word
		for letter in word:
			loc = FOLDER_PREFIX + letter + '/'
			numImg = len(os.listdir(loc)) # determine how many original images were used
			loc = loc + letter + '/'
			numJit = len(os.listdir(loc)) # count total jittered images
			modulus = numJit/numImg # how many new images each jitter op created
			
			if numImg>2:
				rand1 = random.randint(1,numImg-2) # pick from an orginal image set
				rand2 = random.randint(0,modulus-2) # pick one of its jitters
			
				img = Image.open(loc + letter + '_' + str(rand1) + '_' + str(rand2) + '.png')
				# print loc + letter + '_' + str(rand1) + '_' + str(rand2) + '.png'
			else:
				img = Image.new('RGB', img.size, (255, 255, 255))

			temp_bg = Image.new('RGB', img.size, (0, 0, 0))
			temp_bg.paste(img)
			
			indiv_images.append(temp_bg)	
			
		indiv_images.append(Image.new('RGB', img.size, (255, 255, 255)))
		
	#find max width, max height
	max_w, max_h = max_size(indiv_images)
	max_h = max_h+50
	max_w = max_w-5
	
	#create a background to place all images on
	bg_width = OUT_COLUMNS*(max_w) + (2*MARGIN)*max_w
	bg_height = int( math.ceil( len(indiv_images)/float(OUT_COLUMNS) )*(max_h)) + (2*MARGIN)*max_h
	print 'Output Width: ' + str(bg_width), 
	print 'Output Height: ' + str(bg_height)
	background = Image.new('RGB', (bg_width, bg_height), (255, 255, 255))
	
	top_margin = MARGIN*max_h
	left_margin = MARGIN*max_w
	#paste the images into the background
	for i, img in enumerate(indiv_images):
		background.paste(img, (left_margin, top_margin))
		
		#if at end of current line, start a newline
		if (i%OUT_COLUMNS == 0 and i != 0):
			top_margin += max_h
			left_margin = MARGIN*max_w
		else:
			left_margin += max_w
		
	background.save('test.' + OUT_FORMAT, OUT_FORMAT)
	
	
if __name__=='__main__':
	main(sys.argv[1:])
