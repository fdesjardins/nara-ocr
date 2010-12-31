import os, sys, math
import Image, ImageMath

MAX_ROTATION = 20 #degrees cc and ccw
MAX_TRANSLATE = 5 #pixels offset limit
TRANSLATE_DIRS = 8 #number of directions to perform translations
OUT_FORMAT = 'png'
	
def color_to_alpha(image, color=None):
	"Takes a specific color value and changes it to alpha in image" 
	
	image = image.convert('RGBA')
	width, height = image.size

	color = map(float, color)
	img_bands = [band.convert("F") for band in image.split()]

	# Find the maximum difference rate between source and color. 
	alpha = ImageMath.eval(
		"""float(
			max(
				max(
					max(
						difference1(red_band, cred_band),
						difference1(green_band, cgreen_band)
					),
					difference1(blue_band, cblue_band)
				),
				max(
					max(
						difference2(red_band, cred_band),
						difference2(green_band, cgreen_band)
					),
					difference2(blue_band, cblue_band)
				)
			)
		)""",
		difference1=difference1,
		difference2=difference2,
		red_band = img_bands[0],
		green_band = img_bands[1],
		blue_band = img_bands[2],
		cred_band = color[0],
		cgreen_band = color[1],
		cblue_band = color[2]
	)

	# Calculate the new image colors after the removal of the selected color
	new_bands = [
		ImageMath.eval(
			"convert((image - color) / alpha + color, 'L')",
			image = img_bands[i],
			color = color[i],
			alpha = alpha
		)
		for i in xrange(3)
	]

	# Add the new alpha band
	new_bands.append(ImageMath.eval(
		"convert(alpha_band * alpha, 'L')",
		alpha = alpha,
		alpha_band = img_bands[3]
	))

	return Image.merge('RGBA', new_bands)

def difference1(source, color):
	"When source is bigger than color"
	
	return (source - color) / (255.0 - color)

def difference2(source, color):
	"When color is bigger than source"
	
	return (color - source) / color
	
def flatten(lst):
	"Recursively flattens a nested list"
	
	return sum( ([x] if not isinstance(x, list) else flatten(x)
			 for x in lst), [] )
			 
def gen_rotations(img):
	"Receives an image and generates a list of all rotations"

	deltas = range(-1*MAX_ROTATION, 1+MAX_ROTATION, 3) #increment in 3 degrees
	out = [img.rotate(d) for d in deltas]
	return out

def gen_translations(img):
	"Receives an images and generates a list of all translations"
	
	degrees = 360/float(TRANSLATE_DIRS)
	out = []
	
	#list of each degree increment, e.g., if degrees = 90: [0, 90, 180, 270]
	thetas = [degrees*increment for increment in range(0, TRANSLATE_DIRS)] 
	
	#performs translations at each distance, incrementally
	for dist in range(1, MAX_TRANSLATE+1):
	
		#generate a list of affine transformations at this distance
		transformations = [make_affine(dist, theta) for theta in thetas]
		
		#generate all translated images in at this distance
		all_at_this_dist = [img.transform(img.size, Image.AFFINE, t) for t in transformations]
		
		out.append(all_at_this_dist)
		
	return out
	
def main(argv):

	input_images = []
	colored_images = []
	rotations = []
	translations = []
	fixed_edges = []
	output_images = []

	#check for valid image files
	for infile in sys.argv[1:]:
		try:
			im = Image.open(infile)
			print infile, im.format, "%dx%d" % im.size, im.mode
			input_images.append(im)
		except IOError:
			pass
	
	#recolor the black bits to red, and put all the results in colored_images
	for img in input_images:
		background = Image.new('RGB', input_images[0].size, (255, 0, 0))
		image = color_to_alpha(img, (0, 0, 0, 255))
		background.paste(image.convert('RGB'), mask=image)
		colored_images.append(background)
		
	#input_images[0].show()

	#generate all rotated images in range(-1*MAX_ROTATION, 1+MAX_ROTATION)
	rotations = flatten([gen_rotations(img) for img in colored_images])
	
	#generate all translations from each rotated image
	translations = flatten([gen_translations(img) for img in rotations])
	
	#recolor the black bits  around the border to white, and put all the results in fixed_edges
	for img in translations:
		background = Image.new('RGB', input_images[0].size, (255, 255, 255))
		image = color_to_alpha(img, (0, 0, 0, 255))
		background.paste(image.convert('RGB'), mask=image)
		fixed_edges.append(background)
		
	#recolor the red bits, the numbers, back to black, and put all the results in output_images
	for img in fixed_edges:
		background = Image.new('RGB', input_images[0].size, (0, 0, 0))
		image = color_to_alpha(img, (255, 0, 0, 255))
		background.paste(image.convert('RGB'), mask=image)
		output_images.append(background)
	
	prefix = infile[:-4]
	print prefix
	#save images with file names "outfile_1.ppm, outfile_2.ppm, ..."
	for i, img in enumerate(output_images):
		img.save(prefix + '_' + str(i) + '.' + OUT_FORMAT, OUT_FORMAT)

def make_affine(dist, theta):
	"Returns an affine transformation matrix"
	
	#convert to radians from degrees
	theta = math.pi * theta/180.0
	
	x = dist*math.cos(theta)
	y = dist*math.sin(theta)
	
	return (1, 0, x, 0, 1, y)
	
if __name__=='__main__':
	main(sys.argv[1:])
