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

write_image_packed(arg[2] .. '.png', output)

