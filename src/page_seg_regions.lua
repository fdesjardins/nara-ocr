require 'lib.util'
require 'lib.path'
require 'lib.headings'
require 'lib.hocr'
require 'lib.paragraphs'
require "lib.getopt"

opt,arg = util.getopt(arg)

import_all(ocr)
import_all(graphics)
import_all(iulib)

image = bytearray()
output = intarray()

iulib.read_image_gray(image,arg[1])

binarizer = make_BinarizeByOtsu()
binarizer:binarize(image, image)

segmenter = make_SegmentPageByRAST()
segmenter:segment(output, image)

regions = RegionExtractor()
regions:setPageLines(output)

print(regions:length())

for i=0,regions:length()-1 do
	line = bytearray();
	regions:extract(line, image, i, 1);
	write_image_rgb(arg[2] .. i .. '.png', line)
	end

