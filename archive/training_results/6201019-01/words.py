import os, sys

def main(argv):
	
	word_file = open('wordlist', 'r')
	content = word_file.read()
	
	#print content

	valid_words = content.split()
	
	ocr_output = open('cus.out.txt', 'r')
	content = ocr_output.read()
	content_list = content.split()

	for word in content_list:
		print word

	out = [word for word in content_list if word in valid_words]

	#print out, len(out)

if __name__=='__main__':
	main(sys.argv[1:])

