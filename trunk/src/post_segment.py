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

def remove_nontext(img):

	#recolor the black bits to red, and put all the results in colored_images
	background = Image.new('RGB', img.size, (255, 255, 255))
	image = color_to_alpha(img, (255, 255, 0, 255))
	background.paste(image.convert('RGB'), mask=image)

	return background

def ratio_text_nontext(img):
	
	pix = img.load()

	cnt_text = 0
	cnt_nontext = 0

	area = img.size[0]*img.size[1]

	for px in xrange(img.size[0]):
		for py in xrange(img.size[1]):
			if pix[px,py] == (255,255,255) or pix[px,py] == (255,255,0):
				cnt_nontext += 1

	cnt_text = area - cnt_nontext
	return cnt_text/float(cnt_nontext)
