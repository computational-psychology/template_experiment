#!/usr/bin/env python
"""
Script to display a set of stimuli in the experimental monitor

GA.

"""

from hrl import HRL
import numpy as np
import ImageFont, ImageDraw
from PIL import Image
import glob

lut = 'lut.csv'

background = 0.27


def draw_text(text, bg=background, text_color=0, fontsize=48):
    # function from Thorsten
    """ create a numpy array containing the string text as an image. """

    bg *= 255
    text_color *= 255
    font = ImageFont.truetype(
            "/usr/share/fonts/truetype/msttcorefonts/arial.ttf", fontsize,
            encoding='unic')
    text_width, text_height = font.getsize(text)
    im = Image.new('L', (text_width, text_height), bg)
    draw = ImageDraw.Draw(im)
    draw.text((0,0), text, fill=text_color, font=font)
    return np.array(im) / 255.
    
    
def main(files):

    debug=0
    #print debug
    if debug:

        ### HRL Parameters for DESKTOP ###
        graphics='gpu' 
        inputs='keyboard' 

        # Screen GPU
        wdth = 800
        hght = 600
        fs = False   # fullscreen mode off
        scrn = 0     # screen number

    else:
        
        ### HRL Parameters for DATAPIXX ###
        graphics='datapixx' 
        inputs='responsepixx' # or 'responsepixx'

        wdth = 1024
        hght = 768
        fs = True   # fullscreen mode
        scrn = 1    # screen number

    #############################################
    hrl = HRL(graphics=graphics,inputs=inputs, lut =lut, photometer=None, wdth=wdth, hght=hght, bg=background, fs=fs, scrn = scrn)
    
    
    whlf = wdth/2.0
    hhlf = hght/2.0
    #qh = hght/4.0  
    #qw = wdth/4.0
    #ws = wdth/6.0
  
    # reading PNGs and converting to grayscale
    textures = []
    for fname in files:
        
        print "loading... %s " % fname
        ## the image is loaded using PIL module and converted to a 
        ## numpy array ranging from 0 to 1.
        image = Image.open(fname).convert("L")
        im = np.asarray(image)/ 255.    
        
        # texture creation in buffer, input is numpy array [0-1]
        tex = hrl.graphics.newTexture(im)
        textures.append(tex)
    
    # generating text for filenames to be displayed
    texts = []
    for fname in files:
        im = draw_text(fname, bg=0.27, text_color=0, fontsize=20)
        tex = hrl.graphics.newTexture(im)
        texts.append(tex)
    
    #######
    i=0
    #######################################
    while True:
        tex = textures[i]
        tex.draw(( whlf - tex.wdth/2 , hhlf - tex.hght/2))
        
        tex = texts[i]
        tex.draw((100, 100))
        
        hrl.graphics.flip(clr=True)   # clr= True to clear buffer
        print "currently showing: %s" % files[i]
        
        (btn,t1) = hrl.inputs.readButton()
        #print btn
        
        if btn == 'Space':
             break
        elif btn == 'Right':
            i+=1
        elif btn == 'Left':
            i-=1
        
        if i<0:
            i=len(textures)-1
        if i==len(textures):
            i=0
            
    # closing window
    hrl.close()



if __name__ == '__main__':
    
    files = glob.glob('stimuli/demo/*.png')
    main(files)
    
    
# EOF
    
