import sys, os
import Image

def main(argv):
    
    input_images = []
    colored_images = []

    #check fo valid image files
    for infile in argv:
        try:
            im = Image.open(infile)
            print infile, im.format, "%dx%d" % im.size, im.mode
            input_images.append(im)
        except IOError:
            pass

    img = input_images[0]
    for i in input_images:
        if (i.size[0]*i.size[1]) > (img.size[0]*img.size[1]):
            if i.size[0] > 2*i.size[1] and i.size[0] < 3*i.size[1]:
                img = i

    img.show()

if __name__=='__main__':
    args = os.listdir('./')
    main(args)
