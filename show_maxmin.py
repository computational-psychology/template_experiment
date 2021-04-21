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
    
    
def main():

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
        #wdth = 1600
        #hght = 1200 
        #wdth = 2048
        #hght = 1536 
        fs = True   # fullscreen mode
        scrn = 1    # screen number

    #############################################
    hrl = HRL(graphics=graphics,inputs=inputs, lut =lut, photometer=None, wdth=wdth, hght=hght, bg=background, fs=fs, scrn = scrn)
    
    
    whlf = wdth/2.0
    hhlf = hght/2.0
    weht = wdth/8.0
    heht = hght/8.0
  
        
    # texture creation in buffer, input is numpy array [0-1]
    white = hrl.graphics.newTexture(np.array([[1]]))
    black = hrl.graphics.newTexture(np.array([[0]]))
    
    s = 150
    white.draw((whlf - s, hhlf - s),(s, s))
    black.draw((whlf, hhlf - s),(s, s))
    white.draw((whlf, hhlf),(s, s))
    black.draw((whlf - s, hhlf),(s, s))

    hrl.graphics.flip(clr=False)   
    
    #######################################
    while True:
        #hrl.graphics.flip(clr=True)   # clr= True to clear buffer
        
        (btn,t1) = hrl.inputs.readButton()
        #print btn
        
        if btn == 'Space':
             break
            
    # closing window
    hrl.close()



if __name__ == '__main__':
    
    main()
    
    
# EOF
    
