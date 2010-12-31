import sys, os
import Image

sys.path.append('src/')
sys.path.append('pytesser/')

from extractions import *

def main(argv):
    
    ## open input image
    try:
        img = Image.open(argv[0])
        print argv[0], img.format, "%dx%d" % img.size, img.mode
    except IOError:
        pass
    
    os.system('rm -rf temp/*') # clear workspace
    
    ## HEADER
    head = "ISO-10303-21;\n" + \
            "HEADER;\n" + \
            "/* Generated from a scanned image by software \n" + \
            "developed by Forrest Desjardins */\n\n"

    #print '\n' + head

    ## FILE_DESCRIPTION
    desc = get_filedesc_from_image(img)
    description = "FILE_DESCRIPTION(\n" + \
                  "/* description */ ('" + desc[0] + "'),\n" + \
                  "/* implementation level */ '" + desc[1] + "');\n\n"
                
    #print '\n' + description 
    
    ## FILE_NAME
    name = get_filename_from_image(img)
    file_name = "FILE_NAME(\n" + \
                "/* name */ '" + name[0] + "',\n" + \
                "/* time_stamp */ '" + name[1] + "',\n" + \
                "/* author */ ('" + name[2] + "'),\n" + \
                "/* organization */ ('" + name[3] + "'),\n" + \
                "/* preprocessor_version */ '" + name[4] + "'\n" + \
                "/* orginating system */ '" + name[5] + "'\n" + \
                "/* authorization */ '" + name[6] + "');\n\n" 
    
    #print file_name + '\n'

    ## FILE_SCHEMA
    file_schema = "FILE_SCHEMA (('EXPLICIT_DRAUGHTING'));\nENDSEC;\n\n"

    ## DATA
    data = "DATA;\n\nENDSEC;\nEND-ISO-10303-21;"

    ## write to step file
    f = open('step_output/' + argv[0][12:-4] + '.stp', 'w')
    f.write(head)
    f.write(description)
    f.write(file_name)
    f.write(file_schema)
    f.write(data)

'''ISO-10303-21;
HEADER;
FILE_DESCRIPTION(
/* description */ ('A minimal AP214 example with a single part'),
/* implementation_level */ '2;1');
FILE_NAME(
/* name */ 'demo',
/* time_stamp */ '2003-12-27T11:57:53',
/* author */ ('Lothar Klein'),
/* organization */ ('LKSoft'),
/* preprocessor_version */ ' ',
/* originating_system */ 'IDA-STEP',
/* authorization */ ' ');
FILE_SCHEMA (('AUTOMOTIVE_DESIGN { 1 0 10303 214 2 1 1}'));
ENDSEC;
DATA;
#10=ORGANIZATION('O0001','LKSoft','company');
#11=PRODUCT_DEFINITION_CONTEXT('part definition',#12,'manufacturing');
#12=APPLICATION_CONTEXT('mechanical design');
#13=APPLICATION_PROTOCOL_DEFINITION('','automotive_design',2003,#12);
#14=PRODUCT_DEFINITION('0',$,#15,#11);
#15=PRODUCT_DEFINITION_FORMATION('1',$,#16);
#16=PRODUCT('A0001','Test Part 1','',(#18));
#17=PRODUCT_RELATED_PRODUCT_CATEGORY('part',$,(#16));
#18=PRODUCT_CONTEXT('',#12,'');
#19=APPLIED_ORGANIZATION_ASSIGNMENT(#10,#20,(#16));
#20=ORGANIZATION_ROLE('id owner');
ENDSEC;
END-ISO-10303-21;'''

if __name__=='__main__':
    main(sys.argv[1:])
