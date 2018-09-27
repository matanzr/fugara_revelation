import os
import sys
from PIL import Image


def extractFrames(inGif, outFolder):
    if not os.path.exists(outFolder):
        os.makedirs(outFolder)
    
    frame = Image.open(inGif)
    nframes = 0
    while frame:
        frame.save( '%s/%s-%s.png' % (outFolder, os.path.basename(inGif), nframes ) , 'PNG')
        nframes += 1
        try:
            frame.seek( nframes )
        except EOFError:
            break;
    return True
    

# extractFrames(sys.argv[1], sys.argv[2])
extractFrames("/mnt/c/Users/matan/Downloads/gifs_to_use/eyes1.gif", "/mnt/c/Users/matan/Downloads/gifs_to_use/eyes1/")
extractFrames("/mnt/c/Users/matan/Downloads/gifs_to_use/eyes2.gif", "/mnt/c/Users/matan/Downloads/gifs_to_use/eyes2/")
extractFrames("/mnt/c/Users/matan/Downloads/gifs_to_use/eyes3.gif", "/mnt/c/Users/matan/Downloads/gifs_to_use/eyes3/")
extractFrames("/mnt/c/Users/matan/Downloads/gifs_to_use/eyes4.gif", "/mnt/c/Users/matan/Downloads/gifs_to_use/eyes4/")
extractFrames("/mnt/c/Users/matan/Downloads/gifs_to_use/eyes5.gif", "/mnt/c/Users/matan/Downloads/gifs_to_use/eyes5/")
extractFrames("/mnt/c/Users/matan/Downloads/gifs_to_use/eyes6.gif", "/mnt/c/Users/matan/Downloads/gifs_to_use/eyes6/")