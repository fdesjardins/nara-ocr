#include <iulib/iulib.h>
#include <colib/colib.h>
#include <ocropus/ocropus.h>

using namespace iulib;
using namespace colib;
using namespace ocropus;

int main(int argc,char **argv) {
  try {
    bytearray image;
    intarray output;

    read_image_binary(image,argv[1]);

    init_ocropus_components();
    
    autodel<ISegmentPage> segmenter;
    make_component(segmenter, "SegmentPageByVORONOI");

    segmenter->segment(output, image);
    
    write_image_binary(argv[2],image);
  } catch(const char *message) {
    fprintf(stderr,"error: %s\n",message);
    exit(1);
  }
}
