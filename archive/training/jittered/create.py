import os, sys, time

def main(infile):
	print infile
	os.system('convert ' + infile + ' ' + infile[:4] + '.pbm')
	time.sleep(1)
	os.system('convert ' + infile + ' ' + infile[:4] + '.tif')
	time.sleep(1)
	os.system('tesseract ' + infile + ' ' + infile[:4])
	time.sleep(1)
	os.system('tesseract ' + infile + ' ' + infile[:4] + ' batch.nochop makebox')
	time.sleep(1)
	os.system('tessboxes ' + infile[:4] + '.pbm ' + infile[:4] + '.box > ' + infile[:4] + '.ppm')

if __name__=='__main__':
	main(sys.argv[1])
