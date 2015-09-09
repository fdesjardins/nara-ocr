import sys, os

def main(argv):
	f = open(argv[0], 'r')

	all_lines = f.readlines()

	cnt = 0
	for line in all_lines:
		for ch in line:
			if ch != ' ': 
				cnt+=1

	print cnt

if __name__=="__main__":
	main(sys.argv[1:])
