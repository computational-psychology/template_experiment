#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
MLCM experiment for perceived transmittance with varying physical color of the
transparency and physical transmittance


@author: GA Apr 2018
"""

# Package Imports
from hrl import HRL
from hrl.graphics import graphics
# Qualified Imports
import numpy as np
from PIL import Image
import sys
import time
from PIL import Image, ImageFont, ImageDraw


# flag to switch between running locally or running in the lab
inlab = False


# size of Siements monitor
WIDTH=1024
HEIGHT=768

# center of screen
whlf = WIDTH/2.0
hhlf = HEIGHT/2.0


def image_to_array(fname, in_format = 'png'):
    # Function written by Marianne
    """
    read specified image file (default: png), converts it to grayscale and into numpy array
    input:
    ------
    fname       - name of image file
    in_format   - extension (png default)
    output:
    -------
    numpy array
    """
    im = Image.open('%s.%s' %(fname, in_format)).convert('L')
    temp_matrix  = [ im.getpixel(( y, x)) for x in range(im.size[1]) for y in range(im.size[0])]
    temp_matrix  = np.array(temp_matrix).reshape(im.size[1], im.size[0])
    im_matrix    = np.array(temp_matrix.shape,dtype=np.float64)
    im_matrix    = temp_matrix/255.0
    #print im_matrix
    return im_matrix
    
    

        
def read_design(fname):
    # function written by Marianne
    
    design = open(fname)
    header = design.readline().strip('\n').split()
    print header
    data   = design.readlines()
    
    new_data = {}
    
    for k in header:
        new_data[k] = []
    for l in data:
        curr_line = l.strip().split()
        for j, k in enumerate(header):
            new_data[k].append(curr_line[j])
    return new_data


def read_design_csv(fname):
    
    
    design = open(fname)
    header = design.readline().strip('\n').split(',')
    #print header
    data   = design.readlines()
    
    new_data = {}
    
    for k in header:
        new_data[k] = []
    for l in data:
        curr_line = l.strip().split(',')
        for j, k in enumerate(header):
            new_data[k].append(curr_line[j])
    return new_data
    
    
    
def read_response(hrl):
    
    btn = None
    while btn == None or btn == 'Up' or btn == 'Down' :
        (btn,t1) = hrl.inputs.readButton()
        print(btn)
        if  btn == 'Right':
            response = 1
        elif btn == 'Left':
            response = 0
        elif btn == 'Space':
            print 'space'
        if hrl.inputs.checkEscape():
            print 'Abort! Abort!'
            hrl.close()
            sys.exit(0)

    return response, btn, t1

def get_last_trial(vp_id,sess):
    try:
        rfl =open('results/%s/%s_block_%d.txt' %(vp_id, vp_id,  sess), 'r')
    except IOError:
        print 'result file not found'
        return 0
        
    for line in rfl:
        try:
            last_trl = int(line.split('\t')[1])
        except ValueError:
            pass
            
    rfl.close()
    
    if last_trl>0:
        last_trl=last_trl+1
        
    return last_trl
    
def draw_text(text, bg=0.27, text_color=0, fontsize=48):
    # function from Thorsten
    """ create a numpy array containing the string text as an image. """

    bg *= 255
    text_color *= 255
    font = ImageFont.truetype(
            "/usr/share/fonts/truetype/msttcorefonts/arial.ttf", fontsize,
            encoding='unic')
    text_width, text_height = font.getsize(text)
    dims = (text_width, text_height)
    im = Image.new('L', dims, int(bg))
    draw = ImageDraw.Draw(im)
    draw.text((0,0), text, fill=text_color, font=font)
    return np.array(im) / 255.


def show_continue(hrl, b, nb):
    # Function from Thorsten
    hrl.graphics.flip(clr=True)
    if LANG=='de':
        lines = [u'Du kannst jetzt eine Pause machen.',
                 u' ',
                 u'Du hast %d von %d blocks geschafft.' % (b, nb),
                 u' ',
                 u'Zum Weitermachen, druecke die rechte Taste,',
                 u'zum Beenden druecke die linke Taste.'
                 ]
    elif LANG=='en':
        lines = [u'You can take a break now.',
                 u' ',
                 u'You have completed %d out of %d blocks.' % (b, nb),
                 u' ',
                 u'To continue, press the right button,',
                 u'to finish, press the left button.'
                 ]
    else:
        raise('LANG not available')    
        
    for line_nr, line in enumerate(lines):
        textline = hrl.graphics.newTexture(draw_text(line, fontsize=36))
        textline.draw(((1024 - textline.wdth) / 2,
                       (768 / 2 - (4 - line_nr) * (textline.hght + 10))))
    hrl.graphics.flip(clr=True)
    btn = None
    while not (btn == 'Left' or btn == 'Right'):
        (btn,t1) = hrl.inputs.readButton()
    
    # clean text    
    graphics.deleteTextureDL(textline._dlid)    
    
    return btn
        


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


def run_trial(hrl,trl, block,start_trl, end_trl):
    
    whlf = WIDTH/2.0
    hhlf = HEIGHT/2.0

    # clears screen
    hrl.graphics.flip()
    
    # draws fixation dot in the middle
    frm1 = hrl.graphics.newTexture(np.ones((2, 2))*0.0)
    frm1.draw(( whlf, hhlf))
    hrl.graphics.flip()
        
    # sleeps for 250 ms
    time.sleep(0.25)
    
    # 
    print "TRIAL =", trl
    
    #show a break screen automatically after so many trials
    if (trl-start_trl)%80==0 and (trl-start_trl)!=0: 
        show_break(hrl,trl, (start_trl + (end_trl-start_trl)))
    
    # current trial design variables
    thistrial = int(design['Trial'][trl])
    tau1 = float(design['tau1'][trl])
    tau2 = float(design['tau2'][trl])
    alpha1 = float(design['alpha1'][trl])
    alpha2 = float(design['alpha2'][trl])
    
    print tau1
    print alpha1
    print tau2
    print alpha2
    
    # stimuli
    trialname1 = '%d_a_%.2f_tau_%.2f' % (thistrial, alpha1, tau1)
    stim_name1 = 'stimuli/%s/mlcm/block_%d_%s_cropped' % (vp_id, block, trialname1)
        
    trialname2 = '%d_a_%.2f_tau_%.2f' % (thistrial, alpha2, tau2)
    stim_name2 = 'stimuli/%s/mlcm/block_%d_%s_cropped' % (vp_id, block, trialname2)
    

    #print stim_name
    
    # load stimlus image and convert from png to numpy array 
    curr_image1 = image_to_array(stim_name1)
    curr_image2 = image_to_array(stim_name2)

    # texture creation in buffer : stimulus
    checkerboard1 = hrl.graphics.newTexture(curr_image1)
    checkerboard2 = hrl.graphics.newTexture(curr_image2)

    
    # Show stimlus 
    # draw the checkerboard s
    checkerboard1.draw((0, hhlf - checkerboard1.hght/2))
    checkerboard2.draw((whlf, hhlf - checkerboard1.hght/2))
         
    # flip everything
    hrl.graphics.flip(clr=False)   # clr= True to clear buffer
    
    # loop for waiting a response
    no_resp = True 
    while no_resp: # as long as no_resp TRUE
        response, btn, t1 = read_response(hrl)
        print "btn =", btn   
        if btn != None:
               no_resp = False
    
    rfl.write('%d\t%d\t%f\t%f\t%f\t%f\t%d\t%f\t%f\n' % (block, trl, alpha1, alpha2, tau1, tau2, response, t1, time.time()))
    rfl.flush()

    # clean checkerboard texture from buffer
    # (needed! Specially if hundreds of trials are presented, if not 
    # cleared they accummulate in buffer)
    graphics.deleteTextureDL(checkerboard1._dlid)
    graphics.deleteTextureDL(checkerboard2._dlid)

    
    return response
    



### Run Main ###
if __name__ == '__main__':

    LANG ='en' # 'de' or 'en'
    
    # log file name and location
    ## this is the design matrix which is loaded
    vp_id   = raw_input ('Please input the observer name (e.g. demo): ')
    
    ## determines which blocks to run
    # reads block order
    blockorder = read_design('design/%s/mlcm/%s_experiment_order.txt' %(vp_id, vp_id))
    
    # reads the blocks already done
    try:
        blocksdone = read_design('results/%s/mlcm/%s_blocks_done.txt' %(vp_id, vp_id))
        
        # determine which blocks are left to run
        next = len(blocksdone['number'])
        blockstorun = {'number': blockorder['number'][next:], 'block': blockorder['block'][next:]}
        
    except IOError:
        blocksdone  = None
        blockstorun = blockorder  # all blocks to run
        
    # if all is done
    if len(blockstorun['number']) == 0:
        print "All BLOCKS are DONE, exiting."

        
    # opens block file to write 
    bfl = open('results/%s/mlcm/%s_blocks_done.txt' %(vp_id, vp_id), 'a')
    if blocksdone == None:
        block_headers = ['number', 'block']
        bfl.write('\t'.join(block_headers)+'\n')
        bfl.flush()
        
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
				  scrn=1,
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
                  
    # #Iterate across all blocks that need to be presented
    for i in range(len(blockstorun['number'])):
        
        sess = np.int(blockstorun['number'][i])
        print (sess)
        bl = blockstorun['block'][i]
        
        print "Block %d " % (sess)
        
        start_trl = get_last_trial(vp_id, sess)   
                
        # log file name and location
        design = read_design_csv('design/%s/mlcm/block_%d.csv' %(vp_id, sess))
        rfl    = open('results/%s/mlcm/%s_block_%d.txt' %(vp_id, vp_id, sess), 'a')
        
        #  get end trial
        end_trl   = len(design['Trial'])
        

        if start_trl == 0:
            result_headers = ['block', 'trial', 'alpha1', 'alpha2', 'tau1', 'tau2', 'Response', 'resp.time', 'timestamp']
            rfl.write('\t'.join(result_headers)+'\n')
        
         
        # loop over one block
        # ================
        for trl in np.arange(start_trl, end_trl):
            #if trl>2:
            #    break
            run_trial(hrl, trl,sess,  start_trl, end_trl) # function that executes the experiment
            
        # close result file for this block
        rfl.close()
        
        # save the block just done
        if trl==(end_trl-1):
            bfl.write('%d\t%s\n' %(sess, bl))
            bfl.flush()
        
        
        # continue?
        btn = show_continue(hrl, i+1, len(blockstorun['number']))
        print "continue screen, pressed ", btn
        if btn == 'Left':
            break
        
        
    # close block done file
    bfl.close()   
   
    # finishes everything
    hrl.close()
    print "Session exited" 
        
        
# EOF
