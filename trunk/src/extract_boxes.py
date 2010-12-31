#!/usr/bin/python

import sys, os
import Image

def crop_box(box, image):
    w,h = box[2]-box[0], box[3]-box[1]
    print w,h
    bg = Image.new('RGB', (w,h), (255,255,255))
    img = image.crop(box)
    bg.paste(img)
    return bg

def extract_corners(line, image):
    bot_left_x = int(line.split()[1])
    bot_right_y = image.size[1] - int(line.split()[2])
    top_right_x = int(line.split()[3])
    top_left_y = image.size[1] - int(line.split()[4])

    return bot_left_x, top_left_y, top_right_x, bot_right_y

def main(argv):
    
    box_locations = []
    output_images = []

    #try to open the image file
    try:
        im = Image.open(argv[0])
        print im.format, "%d %d" % im.size, im.mode
    except IOError:
        print "Bad image file."
        return

    #try to open the box file
    try:
        box = open(argv[1])
        print box
    except IOError:
        print "Bad box file."
        return

    box_locations = [extract_corners(line,im) for line in box.readlines()]
    output_images = [crop_box(box,im) for box in box_locations]
    [img.save('X_' + str(x) + ".png", "PNG") for x,img in enumerate(output_images)]

if __name__=='__main__':
    main(sys.argv[1:])
