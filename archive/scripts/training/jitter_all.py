#!/usr/bin/python

import sys, os

### employs jitter.py on the images contained in the char_ directories
### usage: "python jitter_all.py" while in the same directory as char_A, char_B, etc

def count_images(location, prefix):
    fnames = os.listdir(location)
    return len([fname for fname in fnames if prefix in fname])

def main():

    dirs = '0123456789ABCDEFGHIJKLMNOPQRSTUVWXYZ'

    for ch in dirs:
        num_imgs = len(os.listdir('char_'+ch))
        mkdir = 'mkdir char_'+ch+'/'+ch
        #print mkdir
        os.system(mkdir)
    
        ## generate jittered images, then organize them
        for i in range(num_imgs):
            jitter = 'python jitter.py '+'char_'+ch+'/'+ch+'_'+str(i)+'.png'
            #print jitter
            os.system(jitter)

            location = 'char_'+ch+'/'
            prefix = ch+'_'+str(i)+'_'
            num_jittered_images = count_images(location, prefix)
            #print num_jittered_images

            ## consolidates the new jittered images
            for j in range(num_jittered_images):
                jit_img = location+ch+'_'+str(i)+'_'+str(j)+'.png'
                new_loc = location+ch
                #print jit_img

                mv = 'mv '+jit_img+' '+new_loc
                os.system(mv)
            
if __name__=='__main__':
    main()
        
