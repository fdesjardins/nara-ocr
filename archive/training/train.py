#!/usr/bin/python

import 	subprocess, os, sys, time

def main(argv):
	
	#create box file from image
	if len(argv)==2 and argv[1] == '-makebox':
		make_box(argv[0])
	else:
                #create .tr file from training tesseract using the box file	
		train(argv[0])

	        #unicharset_extractor
		uchar_extract(argv[0])

	        #mf and cn clustering
		cluster(argv[0])

	        #wordlist2dawg frequent_words_list freq-dawg
	        #wordlist2dawg words_list word-dawg

		#combine_tessdatea
		combine(argv[0])

def cluster(f):
	cmds = []
	cmds.append('mftraining -U unicharset ' + f[:-4] + '.tr')
	cmds.append('cntraining ' + f[:-4] + '.tr')

	for cmd in cmds:
		os.system(cmd)
		time.sleep(2)

def combine(f):
	cmd = 'combine_tessdata ./'
	os.system(cmd)


def make_box(f):
	cmd = 'tesseract ' + f + ' ' + f[:-4] + ' batch.nochop makebox'
	os.system(cmd)


def tessboxes(f):
	cmds = []
	cmds.append('convert ' + f + ' ' + f[:-4] + '.pbm') # convert [inFile] [inFile.pbm] 
	cmds.append('tessboxes ' + f[:-4] + '.pbm' + ' ' + f[:-4] + '.box > ' + f[:-4] + ".ppm") # tessboxes [inFile] [inFile.box] > [inFile.ppm]
	
	for cmd in cmds: 
		os.system(cmd)
		time.sleep(2)


def train(f):
	cmd = 'tesseract ' + f + ' ' + f[:-4] + ' nobatch box.train.stderr'
	os.system(cmd)


def uchar_extract(f):
	cmd = 'unicharset_extractor ' + f[:-4] + '.box'
	os.system(cmd)


if __name__ == "__main__":
	main(sys.argv[1:])
