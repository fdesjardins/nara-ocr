# NARA OCR

> Convert engineering assembly diagrams to ISO 10303 (STEP) files using optical character recognition

Drawings of mechanical assemblies can be processed to yield data-exchange forms
such as STEP files using a combination of optical character recognition and
segmentation algorithms.

## Usage

`python main.py input_images/6201018-01.tif`

## Dependencies

* [pytesser](http://code.google.com/p/pytesser/)
* [tesseract-ocr](http://code.google.com/p/tesseract-ocr/)
* [OCRopus](http://code.google.com/p/ocropus/wiki/InstallTranscript)
* iulib
* ocropus
* ocropy
* ocroswig
* openfst-1.1
* pyopenfst
* tessboxes-0.6+ http://www.lbreyer.com/tessboxes.html
* ImageMagick
* Python Imaging Library (PIL)

## Notes

1. A function should be designed that can identify the region the parts are located in
2. Crop the part list out of the image
3. Use segmentation to remove non-text
4. Segment into regions, which should result in table rows
5. Perform OCR on these rows employing tesseract's dictionary
6. (optional) Run results through spell-checker

All but number 1 have already been accomplished in extracting FILE_NAME and FILE_DESCRIPTION.

One thought: run the entire image through tesseract, and generate a box file. Search this box file for the expected title of the part table (“LIST OF MATERIAL” in these images), and record the coordinates of any matches. From here, a type of segmentation could be used to find the width and height of the title box.

There is already a basic Canny edge detection script that may be useful, and a region growing method could be used, based on pixel intensities.

With the coordinates of the title block, extend this region downward using boxes of the same dimensions as the title block. Check each of these new regions text to non-text ratios, until the ratio is extremely low, signify the end of the table.

The region formed now contains the table “LIST OF MATERIAL”, and now this region can be segmented using RAST, and parts parsed out.

## License

MIT © Forrest Desjardins
