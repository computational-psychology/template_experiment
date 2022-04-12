#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
Asymmetric matching experiment with external, variegatd matching field

Uses HRL on python 2


@authors: CW, GA.
"""

### Imports ###
from helper_functions import image_to_array, read_design, read_design_csv, draw_text
from make_comp_surround import make_life_matches
from hrl import HRL
from hrl.graphics import graphics

import pygame as pg
import OpenGL.GL as gl
import numpy as np
from PIL import Image, ImageFont, ImageDraw
import random, sys, os, time

from socket import gethostname

# flag to switch between running locally or running in the lab
inlab = True if "vlab" in gethostname() else False


# size of Siements monitor
WIDTH=1024
HEIGHT=768


# center of screen
whlf = WIDTH/2.0
hhlf = HEIGHT/2.0


# small and big steps during adjustment 
sms = 0.002
bgs = 0.02


## Functions which are needed for the experiment    
def warning_min(hrl):
    # function that generates a beep tone
    #status=  os.system('beep')
    # print "beep status ", + status
    
    hrl.graphics.flip(clr=True)
    if LANG=='de':
        lines = [u'Minimum erreicht!',
             u' ',
             u'Zum Weitermachen, drücke die mittlere Taste.']

    elif LANG=='en':
         lines = [u'Reached minimum!',
             u' ',
             u'To continue, press the middle button.']
    else:
        raise('LANG not available')
        
    for line_nr, line in enumerate(lines):
        textline = hrl.graphics.newTexture(draw_text(line, fontsize=36))
        textline.draw(((1024 - textline.wdth) / 2,
                       (768 / 2 - (4 - line_nr) * (textline.hght + 10))))
    hrl.graphics.flip(clr=True)
    btn = None
    while btn != 'Space':
        (btn,t1) = hrl.inputs.readButton()
    
def warning_max(hrl):
    # function that generates a beep tone
    #status=  os.system('beep')
    # print "beep status ", + status
    hrl.graphics.flip(clr=True)
    
    if LANG=='de':
        lines = [u'Maximum erreicht!',
             u' ',
             u'Zum Weitermachen, drücke die mittlere Taste.']

    elif LANG=='en':
         lines = [u'Reached maximum!',
             u' ',
             u'To continue, press the middle button.']
    else:
        raise('LANG not available')
        

    for line_nr, line in enumerate(lines):
        textline = hrl.graphics.newTexture(draw_text(line, fontsize=36))
        textline.draw(((1024 - textline.wdth) / 2,
                       (768 / 2 - (4 - line_nr) * (textline.hght + 10))))
    hrl.graphics.flip(clr=True)
    btn = None
    while btn != 'Space':
        (btn,t1) = hrl.inputs.readButton()
    
    
def show_stimulus(hrl, checkerboard, curr_match, match_lum):

    # draw the checkerboard 
    checkerboard.draw (( whlf - checkerboard.wdth/2 , hhlf -  checkerboard.hght/2))
    # print "new_match_lum =", match_lum
    
    # create match stimulus with adjusted luminance
    center_display = show_match(hrl, match_lum, curr_match)
    center_display.draw (( whlf - center_display.wdth/2 , hhlf/4-50))
    
    # flip everything
    hrl.graphics.flip(clr=False)   # clr= True to clear buffer
    
    # delete texture from buffer
    graphics.deleteTextureDL(center_display._dlid)


def adjust_loop(hrl, match_lum, checkerboard, curr_match):
    
    btn = None
    while btn != 'Space':
        (btn,t1) = hrl.inputs.readButton()
        if btn == 'Up':
            match_lum += bgs
            if  match_lum >1:
                 warning_max(hrl)
                 match_lum = 1.0
            elif match_lum < 0:
                 warning_min(hrl)
                 match_lum = 0.0
            show_stimulus(hrl, checkerboard, curr_match, match_lum)
        elif btn == 'Down':
            match_lum -= bgs
            if match_lum >1.0:
                 warning_max(hrl)
                 match_lum  = 1.0
            elif match_lum < 0.0:
                 warning_min(hrl)
                 match_lum = 0.0
            show_stimulus(hrl, checkerboard, curr_match, match_lum)
        elif btn == 'Right':
            match_lum += sms
            if  match_lum >1.0:
                 warning_max(hrl)
                 match_lum = 1.0
            elif match_lum < 0.0:
                 warning_min(hrl)
                 match_lum = 0.0
            show_stimulus(hrl, checkerboard, curr_match, match_lum)
        elif btn == 'Left':
            match_lum -= sms
            if  match_lum >1.0 :
                 warning_max(hrl)
                 match_lum = 1.0
            elif match_lum < 0.0:
                 warning_min(hrl)
                 match_lum = 0.0
            show_stimulus(hrl, checkerboard, curr_match, match_lum)
        elif btn == 'Space':
            print 'space'
            
        #if hrl.inputs.checkEscape():
        elif btn == 'Escape':    
            print 'Escape pressed, exiting experiment!!'
            hrl.close()
            sys.exit(0)
    
    print "MatchLum =", match_lum
    print "Button = ", btn
    
    return match_lum, btn

def show_match(hrl, match_lum, curr_match):
    # replace the center patch on top of the match_display  
    # and adjust it to the matched luminace

    center = np.copy(curr_match)
    center[center <0] = match_lum    
    # create new texture
    center_display = hrl.graphics.newTexture(center)
    return(center_display)

def match_stimulus(trl):
    trial_match, all_surround = make_life_matches(trl)
    # return the one with a -1 at the center patch, so we can easily replace this area later on
    #print all_surround
    return trial_match[-1], all_surround

def get_last_trial(vp_id):
    try:
        rfl =open('results/%s/matching/%s.txt' %(vp_id, vp_id), 'r')
    except IOError:
        print 'result file not found'
        return 0
        
    for line in rfl:
        try:
            last_trl = int(line.split('\t')[0])
        except ValueError:
            pass
    
    if last_trl>0:
        last_trl=last_trl+1
        
    return last_trl
    

def show_break(hrl,trial, total_trials):
    # Function from Thorsten
    hrl.graphics.flip(clr=True)
    
    if LANG=='de':
        lines = [u'Du kannst jetzt eine Pause machen.',
             u' ',
             u'Du hast %d von %d Durchgängen geschafft.' % (trial,
                 total_trials),
             u' ',
             u'Wenn du bereit bist, drücke die mittlere Taste.'
             ]
    elif LANG=='en':
         lines = [u'You can take a break now.',
             u' ',
             u'You have completed %d out of %d trials.' % (trial,
                 total_trials),
             u' ',
             u'When you are ready, press the middle button.'
             ]
    else:
        raise('LANG not available')
        
    for line_nr, line in enumerate(lines):
        textline = hrl.graphics.newTexture(draw_text(line, fontsize=36))
        textline.draw(((1024 - textline.wdth) / 2,
                       (768 / 2 - (4 - line_nr) * (textline.hght + 10))))
    hrl.graphics.flip(clr=True)
    btn = None
    while btn != 'Space':
        (btn,t1) = hrl.inputs.readButton()
    # clean text    
    graphics.deleteTextureDL(textline._dlid)   
    

def run_trial(hrl,trl, start_trl, end_trl):
    # function written by Torsten and edited by Christiane, reused by GA
    # read out variable values for each trial from the design matrix
    print "TRIAL =", trl
    
    #show break automatically, define after how many trials
    if (trl-start_trl)%50==0:
        show_break(hrl,(trl-start_trl), (end_trl-start_trl))
    
    # get values from design matrix for current trial
    context, r, Trial = design['context'][trl], float(design['r'][trl]), int(design['Trial'][trl])
    
    # use these variable values to define test stimulus (name corresponds to design matrix and name of saved image)
    trialname = '%d_%s_%.2f' % (Trial, context, r)
    stim_name = 'stimuli/%s/matching/%s' % (vp_id , trialname)
    
    #print "r =", r
    
    # load stimlus image and convert from png to numpy array 
    curr_image = image_to_array(stim_name)
    
    # texture creation in buffer : stimulus
    checkerboard = hrl.graphics.newTexture(curr_image)
    
    # random assignment of start match intensity between 0 and 1
    start_idx = random.random()
    no_match       = True 
    match_lum      = start_idx

    # generate match stimulus
    trial_match, all_surround = match_stimulus(trl)

    t1 = time.time()
    while no_match: # as long as no_match TRUE

        curr_match = np.array(trial_match.shape, dtype=np.float64)
        curr_match = trial_match/255. 
        #print curr_match[60]
        
        # Show stimulus and match
        show_stimulus(hrl, checkerboard, curr_match, match_lum)      
  
        # adjust the lumiance
        match_lum, btn = adjust_loop(hrl, match_lum, checkerboard, curr_match)
        print "btn =", btn   
        if btn == 'Space':
               no_match = False
    
    t2 = time.time()
    resptime = t2 - t1
    timestamp = time.time()
    
    rfl.write('%d\t%s\t%s\t%f\t%f\t%f\t%f\t%f\n' %(Trial, context, stim_name, r, start_idx, match_lum, resptime, timestamp))
    rfl.flush()

    # surround information of matching patch should be written together with matched value
    fid_all_match.write('%d\t%d\t%d\t%d\t%d\t%d\t%d\t%d\t%d\t%d\t%d\t%d\t%d\t%d\t%d\t%d\t%d\t%d\t%d\t%d\t%d\t%d\t%d\t%d\n' %(all_surround[0,0], all_surround[0,1], all_surround[0,2], all_surround[0,3], all_surround[0,4], all_surround[1,0], all_surround[1,1], all_surround[1,2], all_surround[1,3], all_surround[1,4], all_surround[2,0], all_surround[2,1],  all_surround[2,3], all_surround[2,4], all_surround[3,0], all_surround[3,1], all_surround[3,2], all_surround[3,3], all_surround[3,4], all_surround[4,0], all_surround[4,1], all_surround[4,2], all_surround[4,3], all_surround[4,4]))
    fid_all_match.flush()

    # screenshooting
    #gl.glReadBuffer(gl.GL_FRONT)
    #pixels = gl.glReadPixels(0,0, WIDTH, HEIGHT, gl.GL_RGB, gl.GL_UNSIGNED_BYTE)
    
    #image = Image.fromstring("RGB", (WIDTH, HEIGHT), pixels)
    #image = image.transpose( Image.FLIP_TOP_BOTTOM)
    #image.save('screenshot_%d.png' % trl)
        
    # clean checkerboard texture    
    graphics.deleteTextureDL(checkerboard._dlid)
    
    return match_lum
    


### Run Main ###
if __name__ == '__main__':
    
    LANG ='en' # 'de' or 'en'
    
    vp_id   = raw_input ('Bitte geben Sie Ihre Initialen ein (z.B. demo): ')
    
    # get last trial from results file, to be able to resume from that trial onwards
    start_trl = get_last_trial(vp_id)   
    
    # read design file and open result file for saving 
    design = read_design_csv('design/%s/matching/%s_matching.csv' %(vp_id, vp_id))
    
    #  get last trial (total number of trials)
    end_trl   = len(design['Trial'])
    
    # results file
    rfl    = open('results/%s/matching/%s.txt' %(vp_id, vp_id), 'a')

    # file to save surround of match check
    fid_all_match = open('results/%s/matching/%s_all_match_surr.txt' %(vp_id, vp_id), 'a')

    if start_trl == 0:
        #fid_match.write('b2\tc2\td2\td3\td4\tc4\tb4\tb3\n')
        result_headers = ['trial','context', 'image.fname', 'r', 'start_idx', 'match_lum', 'resp.time', 'timestamp']
        rfl.write('\t'.join(result_headers)+'\n')
 
    # Pass this to HRL if we want to use gamma correction.
    lut = 'lut.csv'   
    
    if inlab:
        ## create HRL object
        hrl = HRL(graphics='datapixx',
                  inputs='responsepixx',
                  photometer=None,
                  wdth=WIDTH,
                  hght=HEIGHT,
                  bg=0.27,
                  scrn="0.1",
                  lut=lut,
                  db = False,
                  fs=True)

    else: 
        hrl = HRL(graphics='gpu',
                  inputs='keyboard',
                  photometer=None,
                  wdth=WIDTH,
                  hght=HEIGHT,
                  bg=0.27,
                  scrn=1,
                  lut=lut,
                  db = True,
                  fs=False)
                    
    
    # loop over trials in design file
    # ================================
    for trl in np.arange(start_trl, end_trl):
        run_trial(hrl, trl, start_trl, end_trl) # function that executes the experiment
        
        
    hrl.close()
    print "Session complete"
    rfl.close()


