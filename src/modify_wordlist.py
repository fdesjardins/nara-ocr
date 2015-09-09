import sys, os
import re

okchars = re.compile('[A-Za-z0-9 ]')

def main(argv):
    try: f = open(argv[0], 'r')
    except IOError: pass

    lines = f.readlines()
    out_lines = []
    newline = ''
    
    for line in lines:
        for ch in line:
            
            if okchars.match(ch):
                newline = newline+ch.upper()
            
        out_lines.append(newline)
        newline = ''

    out = open(argv[0]+'_out', 'w')
    [out.write(line+'\n') for line in out_lines]

if __name__=='__main__':
    main(sys.argv[1:])
