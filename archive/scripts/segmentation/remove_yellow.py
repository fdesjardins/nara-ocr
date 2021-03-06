import os, sys, math
import Image, ImageMath

OUT_FORMAT = 'png'

def difference1(source, color):
	"When source is bigger than color"
	
	return (source - color) / (255.0 - color)

def difference2(source, color):
	"When color is bigger than source"
	
	return (color - source) / color

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

def main(argv):

	input_images = []
	colored_images = []

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
		background = Image.new('RGB', input_images[0].size, (255, 255, 255))
		image = color_to_alpha(img, (255, 255, 0, 255))
		background.paste(image.convert('RGB'), mask=image)
		colored_images.append(background)

	prefix = infile[:-4]

	#save images with file names "outfile_1.ppm, outfile_2.ppm, ..."
	for i, img in enumerate(colored_images):
		img.save(prefix + '_' + str(i) + '.' + OUT_FORMAT, OUT_FORMAT)

if __name__=='__main__':
	main(sys.argv[1:])
