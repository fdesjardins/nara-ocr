import io, sys
import re           #reg ex

from utils import *
from pyaspell import *

def main(argv):
    
    input_result_fs = []
    input_result_contents = []
    input_dict_fs = []
    input_dict_contents = []

    flat_result_contents = []
    split_result_contents = []

    flat_dict_contents = []
    split_dict_contents = []

    ## open our files
    try:
        for param in argv:
            if param[:2] == '-d':
                input_dict_fs.append(open(param[3:], 'r'))
            else:
                input_result_fs.append(open(param, 'r'))

    except IOError:
        print "Invalid dictionary."
        pass

    [input_result_contents.append(f.readlines()) for f in input_result_fs]
    [input_dict_contents.append(f.readlines()) for f in input_dict_fs]
    
    flat_result_contents = flatten(input_result_contents) # useful to have this flattened
    flat_result_contents = [w.rstrip() for w in flat_result_contents] # space and \r chars

    flat_dict_contents = flatten(input_dict_contents) # easier to use as a flattened list
    flat_dict_contents = [w.rstrip() for w in flat_dict_contents] # strip space and \r chars

    ## split up multiple word entries
    for entry in flat_result_contents:
        if len(entry.split()) > 1:
            [split_result_contents.append(w) for w in entry.split()]
        else:
            split_result_contents.append(entry)
    
    ## split up multiple word entries in dict
    for entry in flat_dict_contents:
        if len(entry.split()) > 1:
            [split_dict_contents.append(w) for w in entry.split()]
        else:
            split_dict_contents.append(entry)

    split_dict_contents = [word for word in split_dict_contents if not number_in(word)] #remove numbers
    split_result_contents = [remove_non_chars(word) for word in split_result_contents] #remove non chars
    split_result_contents = [word for word in split_result_contents if not word == ''] #remove blank words

    a = AspellLinux()

    for entry in split_dict_contents:
        #print entry
        a.personal_dict(entry)

    a.personal_dict('ORIGINAL')
    a.personal_dict('ISSUE')
    a.personal_dict('MATERIAL')
    
    #print a.personal_dict()
    out = ''
    
    for word in split_result_contents:
        if len(word) > 2: 
            for sugg in a.suggest(word):
                if sugg in a.personal_dict() and len(sugg) > 2:
                    out += sugg + ' '

    print split_result_contents
    print out

def direct_match(word, dict_word):

    ret = False

    if word == dict_word:
        ret = True

    return ret

def number_in(word):
    
    #word is a number
    try:
        float(word)
        return True
    except ValueError:
        pass

    #word contains a number
    for ch in word:
        try: 
            float(ch)
            return True
        except ValueError:
            continue

def remove_non_chars(word):
    chars = re.compile('[a-zA-Z]')
    
    out = ''
    for ch in word:
        if chars.match(ch):
            out += ch

    return out

if __name__=='__main__':
    main(sys.argv[1:])
