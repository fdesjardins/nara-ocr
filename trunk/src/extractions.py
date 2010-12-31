import sys, os
import Image

from post_segment import *
from pytesser import *
from time import gmtime, localtime, strftime
from utils import *

RATIO_TEXT_NONTEXT = 0.05 # threshold for identifying type of drawing

INFO_BLOCK_COORDS = (6900,4800,8365,5640) # lower-left block
MMC_SHEET1_COORDS = (7400,5700,8250,5780) # mmc drawing number, sheet1
MMC_SHEET2_COORDS = (7360,5390,8350,5475) # mmc drawing number, sheet2
NAVSEA_COORDS = (8345,4480,8450,5003) # navsea drawing number

## coords based on info_block, not whole image
NAME_COORDS = (550,250,1300,550) # name
ORG_COORDS = (0,125,500,250)


def get_desc(info_block, mmc_dwg_no, navsea_dwg_no):

    ## determine layout version, and grab mmc drawing number
    ratio = ratio_text_nontext(info_block)
    if ratio >= RATIO_TEXT_NONTEXT: layout = 'sheet1'     
    else:  layout = 'sheet2'

    ## save for additional segmenting
    info_block.save('temp/info_block_get_desc.png', 'PNG')
    mmc_dwg_no.save('temp/mmc_dwg_get_desc.png', 'PNG')
    navsea_dwg_no.save('temp/navsea_dwg_get_desc.png', 'PNG')

    ## create folders for each
    try:
        os.mkdir('temp/info_block_seg')
        os.mkdir('temp/mmc_dwg_seg')
        os.mkdir('temp/navsea_seg')
    except: pass

    ## perform segmentation into regions
    os.system('ocroscript src/page_seg_regions.lua temp/info_block_get_desc.png temp/info_block_seg/') # info block
    os.system('ocroscript src/page_seg_regions.lua temp/mmc_dwg_get_desc.png temp/mmc_dwg_seg/') # mmc dwg no
    os.system('ocroscript src/page_seg_regions.lua temp/navsea_dwg_get_desc.png temp/navsea_seg/') # navsea dwg no

    ## perform recognition on regions
    os.system('tesseract temp/info_block_seg/2.png temp/contract_no nobatch config/contract_no')
    os.system('tesseract temp/mmc_dwg_seg/1.png temp/mmc_no nobatch config/mmc_no')

    last = len(os.listdir('temp/navsea_seg/')) # number of files
    os.system('tesseract temp/navsea_seg/' + str(last-1) + '.png temp/navsea_no nobatch config/digits')

    ## read values from recognition output
    if layout == 'sheet1':
        contract_no = open('temp/contract_no.txt','r').readlines()[0].rstrip()
    else: contract_no = ' '

    mmc_no = open('temp/mmc_no.txt','r').readlines()[0].rstrip()
    navsea_no = open('temp/navsea_no.txt','r').readlines()[0].rstrip()

    #print contract_no
    #print mmc_no
    #print navsea_no

    description = 'CONTRACT NO ' + contract_no + ' / ' + mmc_no + ' / NAVSEA NO ' + navsea_no

    ## return (description, implementation level)
    ## implementation level = 2;1 for external mapping of complex entity instances.
    return (description, '2;1')

def get_filedesc_from_image(img):

    info_block = get_info_block_img(img, 2)
    mmc_dwg_no = get_mmc_dwg_no_img(img, 2)
    navsea_dwg_no = get_navsea_dwg_no_img(img, 2)

    # info_block.show()
    # navsea_dwg_no.show()
    # mmc_dwg_no.show()

    return get_desc(info_block, mmc_dwg_no, navsea_dwg_no)
    

def get_filename(infoblock):
    
    ## crop and save name area
    name_img = infoblock.crop(NAME_COORDS)
    name_img.save('temp/name.png', 'PNG')

    name = ''
    ## run tesseract for name and concatenate results
    os.system('tesseract temp/name.png temp/name nobatch config/chars')
    name_list = [line.split() for line in open('temp/name.txt', 'r').readlines()] # remove whitespaces
    name_list = flatten(name_list)
    for line in name_list[:-1]: name += line + ' '
    name += name_list[-1]

    #print name_list

    ## create time_stamp
    if gmtime().tm_hour < 12: offset = localtime().tm_hour - (gmtime().tm_hour + 24)
    else: offset = localtime().tm_hour - gmtime().tm_hour
    time_stamp = strftime("%Y-%m-%dT%H:%M:%S"+str(offset)+":00")

    ## author
    author = ''

    ## crop and save organization
    org_img = infoblock.crop(ORG_COORDS)
    org_img.save('temp/org_info.png', 'PNG')
    
    org_info = ''
    ## run tesseract for org_info and concatenate results
    os.system('tesseract temp/org_info.png temp/org_info nobatch config/chars')
    org_list = [line.split() for line in open('temp/org_info.txt', 'r').readlines()] # remove whitespaces
    org_list = flatten(org_list)
    for line in org_list[:-1]: org_info += line + ' '
    org_info += org_list[-1]

    ## return (name, time_stamp, author, organization, preproceessor_version, orginating_system, authorization)
    return (name,time_stamp,author,org_info,'','','')

def get_filename_from_image(img):
    info_block = get_info_block_img(img, 2) 
    # info_block.show()
    return get_filename(info_block)

## segmented == 0: none
## segmented == 1: RAST
## segmented == 2: RAST + remove nontext segments
def get_info_block_img(img, segmented=0):

    ## open info block
    info_block = img.crop(INFO_BLOCK_COORDS)
    info_block.save('temp/info_block.png', 'PNG')

    ## save and segment
    if segmented == 1 or segmented == 2:
        os.system('ocroscript src/page_seg.lua temp/info_block.png temp/info_seg')
        info_block = Image.open('temp/info_seg.png')
    
    ## remove nontext
    if segmented == 2:
        info_block = remove_nontext(info_block)

    return info_block

## segmented == 0: none
## segmented == 1: RAST
## segmented == 2: RAST + remove nontext segments
def get_mmc_dwg_no_img(img, segmented=0):

    ## open info block in lower left corner to determine layout version
    info_block = img.crop(INFO_BLOCK_COORDS)
    info_block.save('temp/info_block.png', 'PNG')
    os.system('ocroscript src/page_seg.lua temp/info_block.png temp/info_seg')
    info_seg = Image.open('temp/info_seg.png')

    ## determine layout version, and grab mmc drawing number
    ratio = ratio_text_nontext(info_seg)
    if ratio >= RATIO_TEXT_NONTEXT: 
        layout = 'sheet1'     
        mmc_dwg_no = img.crop(MMC_SHEET1_COORDS)
    else: 
        layout = 'sheet2'
        mmc_dwg_no = img.crop(MMC_SHEET2_COORDS)

    ## if segmented = 1, save and perform RAST segmentation
    if segmented == 1 or segmented == 2:
        mmc_dwg_no.save('temp/mmc_dwg.png', 'PNG')
        os.system('ocroscript src/page_seg.lua temp/mmc_dwg.png temp/mmc_seg')
        mmc_dwg_no = Image.open('temp/mmc_seg.png')

    ## if segmented = 2, remove nontext
    if segmented == 2:
        mmc_dwg_no = remove_nontext(mmc_dwg_no)
    
    return mmc_dwg_no

## segmented == 0: none
## segmented == 1: RAST
## segmented == 2: RAST + remove nontext segments
def get_navsea_dwg_no_img(img, segmented=0):
    
    ## crop image, rotate, and save
    navsea_dwg_no = img.crop(NAVSEA_COORDS)
    navsea_dwg_no.rotate(-90).save('temp/navsea_dwg.png', 'PNG')

    ## if segmented = 1, save and perform RAST segmentation
    if segmented == 1 or segmented == 2:
        os.system('ocroscript src/page_seg.lua temp/navsea_dwg.png temp/navsea_seg')
        navsea_dwg_no = Image.open('temp/navsea_seg.png')

    ## if segmented = 2, remove nontext
    if segmented == 2:
        navsea_dwg_no = remove_nontext(navsea_dwg_no)

    return navsea_dwg_no
        
def main(argv):
    
    ## open input image
    try:
        img = Image.open(argv[0])
        print argv[0], img.format, "%dx%d" % img.size, img.mode
    except IOError:
        pass
    
    action = {'description': get_desc}
    out = action[argv[1]](img)

    print out

if __name__=='__main__':
    main(sys.argv[1:])
