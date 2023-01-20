#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
Template code for an MLCM experiment

Uses HRL on python 3

@author: GA Apr 2018, updated Nov 2022
"""
# needed for Eyelink eyetracker.
# Install Eyelink Developer Kit and pylink with pip
# See official documentation from SR Research
import pylink
from CalibrationGraphicsPygame import CalibrationGraphics

# Package Imports
from hrl import HRL
from hrl.graphics import graphics
import pygame

import numpy as np
from PIL import Image, ImageFont, ImageDraw
import sys, os, time
from string import ascii_letters, digits
from socket import gethostname

inlab_siemens = True if "vlab" in gethostname() else False
inlab_viewpixx =  True if "viewpixx" in gethostname() else False


dummy_mode = True # True or False. Dummy mode is to test code without using eyetracker


if inlab_siemens:
    # size of Siements monitor
    WIDTH = 1024
    HEIGHT = 768
    bg_blank = 0.1 # corresponding to 50 cd/m2 approx
    middlegap = 0

elif inlab_viewpixx:
    # size of VPixx monitor
    WIDTH = 1920
    HEIGHT = 1080
    bg_blank = 0.27 # corresponding to 50 cd/m2 approx
    middlegap = 150 # pixels

else:
    WIDTH = 1920
    HEIGHT = 1080
    bg_blank = 0.27
    middlegap = 150 # pixels

# center of screen
whlf = WIDTH / 2.0
hhlf = HEIGHT / 2.0



def image_to_array(fname, in_format = 'png'):
    # Function written by Marianne
    """
    Reads the specified image file (default: png), converts it to grayscale
    and into a numpy array

    Input:
    ------
    fname       - name of image file
    in_format   - extension (png default)

    Output:
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
    print(header)
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
    while btn == None or btn == 'Up' or btn == 'Down' or  btn == 'Space':
        (btn,t1) = hrl.inputs.readButton()
        print(btn)
        if  btn == 'Right':
            response = 1
        elif btn == 'Left':
            response = 0
        elif btn == 'Escape':
            response = None
            print('Escape pressed, exiting experiment!!')
            hrl.close()
            sys.exit(0)

    return response, btn, t1

def get_last_trial(vp_id,sess):
    try:
        rfl =open('results/%s/block_%d.csv' % (vp_id,  sess), 'r')
    except IOError:
        print('result file not found')
        return 0

    for line in rfl:
        try:
            last_trl = int(line.split(',')[1])
        except ValueError:
            pass

    rfl.close()

    if last_trl>0:
        last_trl=last_trl+1

    return last_trl

def draw_text(text, bg=bg_blank, text_color=0, fontsize=48):
    # function from Thorsten
    """ create a numpy array containing the string text as an image. """

    bg *= 255
    text_color *= 255
    font = ImageFont.truetype(
            "/usr/share/fonts/truetype/msttcorefonts/arial.ttf", fontsize,
            encoding='unic')
    text_width, text_height = font.getsize(text)
    im = Image.new('L', (text_width, text_height), int(bg))
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
        textline = hrl.graphics.newTexture(draw_text(line, bg=bg_blank, fontsize=36))
        textline.draw(((WIDTH - textline.wdth) / 2,
                       (HEIGHT / 2 - (4 - line_nr) * (textline.hght + 10))))
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
        textline = hrl.graphics.newTexture(draw_text(line, bg=bg_blank, fontsize=36))
        textline.draw(((WIDTH - textline.wdth) / 2,
                       (HEIGHT / 2 - (4 - line_nr) * (textline.hght + 10))))
    hrl.graphics.flip(clr=True)
    btn = None
    while btn != 'Space':
        (btn,t1) = hrl.inputs.readButton()
    # clean text
    graphics.deleteTextureDL(textline._dlid)


def run_trial(hrl,trl, block,start_trl, end_trl):

    whlf = WIDTH/2.0
    hhlf = HEIGHT/2.0

    hrl.graphics.flip(clr=True)

    # draws fixation dot in the middle
    frm1 = hrl.graphics.newTexture(np.ones((2, 2))*0.0)
    frm1.draw(( whlf, hhlf))
    hrl.graphics.flip(clr=True)

    # sleeps for 250 ms
    time.sleep(0.25)

    #
    print("TRIAL =", trl)

    #show a break screen automatically after so many trials
    if (trl-start_trl)%80==0 and (trl-start_trl)!=0:
        show_break(hrl,trl, (start_trl + (end_trl-start_trl)))

    # current trial design variables
    thistrial = int(design['Trial'][trl])
    tau1 = float(design['tau1'][trl])
    tau2 = float(design['tau2'][trl])
    alpha1 = float(design['alpha1'][trl])
    alpha2 = float(design['alpha2'][trl])

    print(tau1)
    print(alpha1)
    print(tau2)
    print(alpha2)

    # stimuli
    trialname1 = '%d_a_%.2f_tau_%.2f' % (thistrial, alpha1, tau1)
    stim_name1 = 'stimuli/%s/block_%d_%s_cropped' % (vp_id, block, trialname1)

    trialname2 = '%d_a_%.2f_tau_%.2f' % (thistrial, alpha2, tau2)
    stim_name2 = 'stimuli/%s/block_%d_%s_cropped' % (vp_id, block, trialname2)


    #print stim_name

    # load stimlus image and convert from png to numpy array
    curr_image1 = image_to_array(stim_name1)
    curr_image2 = image_to_array(stim_name2)

    # texture creation in buffer : stimulus
    checkerboard1 = hrl.graphics.newTexture(curr_image1)
    checkerboard2 = hrl.graphics.newTexture(curr_image2)


    # Show stimlus
    # draw the checkerboard s
    checkerboard1.draw(((whlf - checkerboard1.wdth - middlegap/2), hhlf - checkerboard1.hght/2))
    checkerboard2.draw((whlf + middlegap/2, hhlf - checkerboard1.hght/2))

    # flip everything
    hrl.graphics.flip(clr=False)   # clr= True to clear buffer

    # loop for waiting a response
    no_resp = True
    while no_resp: # as long as no_resp TRUE
        response, btn, t1 = read_response(hrl)
        print("btn =", btn)
        if btn != None:
            no_resp = False

    line = ','.join([str(block), str(trl), str(alpha1), str(alpha2), str(tau1),
                    str(tau2), str(response), str(t1), str(time.time())])

    line +='\n'
    rfl.write(line)
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
    vp_id   = input ('Please input the observer name (e.g. demo): ')

    ## determines which blocks to run
    # reads block order
    blockorder = read_design_csv('design/%s/experiment_order.csv' % vp_id)

    # check if results folder exist, if not, creates
    results_folder = 'results'
    if not os.path.exists(results_folder):
        os.makedirs(results_folder)

    results_folder = 'results/%s' % vp_id
    if not os.path.exists(results_folder):
        os.makedirs(results_folder)

    # reads the blocks already done
    try:
        blocksdone = read_design_csv('results/%s/blocks_done.csv' % vp_id)

        # determine which blocks are left to run
        next = len(blocksdone['number'])
        blockstorun = {'number': blockorder['number'][next:], 'block': blockorder['block'][next:]}

    except IOError:
        blocksdone  = None
        blockstorun = blockorder  # all blocks to run

    # if all is done
    if len(blockstorun['number']) == 0:
        print("All BLOCKS are DONE, exiting.")


    # opens block file to write
    bfl = open('results/%s/blocks_done.csv'% vp_id,'a')
    if blocksdone == None:
        block_headers = ['number', 'block']
        bfl.write(','.join(block_headers)+'\n')
        bfl.flush()

    ###########################################################################
    # TODO: For the eyetracker we need to set a EDF filename, length no more than 8 characthers
    # and no special characthers
    edf_fname = '%s01' % vp_id # CHANGE THIS because it will override

    # check if the filename is valid (length <= 8 & no special char)
    allowed_char = ascii_letters + digits + '_'
    if not all([c in allowed_char for c in edf_fname]):
        raise(RuntimeError, 'ERROR: Invalid EDF filename')
    elif len(edf_fname) > 8:
        raise(RuntimeError, 'ERROR: EDF filename should not exceed 8 characters')

    # We download EDF data file from the EyeLink Host PC to the local hard
    # drive at the end of each testing session, here we rename the EDF to
    # include session start date/time
    time_str = time.strftime("_%Y_%m_%d_%H_%M", time.localtime())
    session_identifier = edf_fname + time_str

    # Step 1: Connect to the EyeLink Host PC
    if dummy_mode:
        el_tracker = pylink.EyeLink(None)
    else:
        try:
            el_tracker = pylink.EyeLink("100.1.1.1")
        except RuntimeError as error:
            print('ERROR:', error)
            sys.exit()


    # Step 2: Open an EDF data file on the Host PC
    edf_file = edf_fname + ".EDF"
    try:
        el_tracker.openDataFile(edf_file)
    except RuntimeError as err:
        print('ERROR:', err)
        # close the link if we have one open
        if el_tracker.isConnected():
            el_tracker.close()
        sys.exit()

    # Add a header text to the EDF file to identify the current experiment name
    # This is OPTIONAL. If your text starts with "RECORDED BY " it will be
    # available in DataViewer's Inspector window by clicking
    # the EDF session node in the top panel and looking for the "Recorded By:"
    # field in the bottom panel of the Inspector.
    preamble_text = 'RECORDED BY %s' % os.path.basename(__file__)
    el_tracker.sendCommand("add_file_preamble_text '%s'" % preamble_text)

    # Step 3: Configure the tracker
    #
    # Put the tracker in offline mode before we change tracking parameters
    el_tracker.setOfflineMode()

    # Get the software version:  1-EyeLink I, 2-EyeLink II, 3/4-EyeLink 1000,
    # 5-EyeLink 1000 Plus, 6-Portable DUO
    eyelink_ver = 0  # set version to 0, in case running in Dummy mode
    if not dummy_mode:
        vstr = el_tracker.getTrackerVersionString()
        eyelink_ver = int(vstr.split()[-1].split('.')[0])
        # print out some version info in the shell
        print('Running experiment on %s, version %d' % (vstr, eyelink_ver))

    # File and Link data control
    # what eye events to save in the EDF file, include everything by default
    file_event_flags = 'LEFT,RIGHT,FIXATION,SACCADE,BLINK,MESSAGE,BUTTON,INPUT'
    # what eye events to make available over the link, include everything by default
    link_event_flags = 'LEFT,RIGHT,FIXATION,SACCADE,BLINK,BUTTON,FIXUPDATE,INPUT'
    # what sample data to save in the EDF data file and to make available
    # over the link, include the 'HTARGET' flag to save head target sticker
    # data for supported eye trackers
    if eyelink_ver > 3:
        file_sample_flags = 'LEFT,RIGHT,GAZE,HREF,RAW,AREA,HTARGET,GAZERES,BUTTON,STATUS,INPUT'
        link_sample_flags = 'LEFT,RIGHT,GAZE,GAZERES,AREA,HTARGET,STATUS,INPUT'
    else:
        file_sample_flags = 'LEFT,RIGHT,GAZE,HREF,RAW,AREA,GAZERES,BUTTON,STATUS,INPUT'
        link_sample_flags = 'LEFT,RIGHT,GAZE,GAZERES,AREA,STATUS,INPUT'
    el_tracker.sendCommand("file_event_filter = %s" % file_event_flags)
    el_tracker.sendCommand("file_sample_data = %s" % file_sample_flags)
    el_tracker.sendCommand("link_event_filter = %s" % link_event_flags)
    el_tracker.sendCommand("link_sample_data = %s" % link_sample_flags)

    # Optional tracking parameters
    # Sample rate, 250, 500, 1000, or 2000, check your tracker specification
    # if eyelink_ver > 2:
    #     el_tracker.sendCommand("sample_rate 1000")
    # Choose a calibration type, H3, HV3, HV5, HV13 (HV = horizontal/vertical),
    el_tracker.sendCommand("calibration_type = HV9")
    # Set a gamepad button to accept calibration/drift check target
    # You need a supported gamepad/button box that is connected to the Host PC
    el_tracker.sendCommand("button_function 5 'accept_target_fixation'")
    ###########################################################################


    # We create the HRL object with parameters that depend on the setup we are using
    if inlab_siemens:
        # create HRL object
        hrl = HRL(
            graphics="datapixx",
            inputs="responsepixx",
            photometer=None,
            wdth=WIDTH,
            hght=HEIGHT,
            bg=bg_blank,
            scrn=1,
            lut='lut.csv',
            db=True,
            fs=True,
        )
    elif inlab_viewpixx:

        hrl = HRL(
            graphics="viewpixx",
            inputs="responsepixx",
            photometer=None,
            wdth=WIDTH,
            hght=HEIGHT,
            bg=bg_blank,
            scrn=1,
            lut='lut_viewpixx.csv',
            db=True,
            fs=True,
        )

    else:
        hrl = HRL(
            graphics="gpu",
            inputs="keyboard",
            photometer=None,
            wdth=WIDTH,
            hght=HEIGHT,
            bg=bg_blank,
            scrn=0,
            lut=None,
            db=True,
            fs=False,
        )

    ###########################################################################
    # Pass the display pixel coordinates (left, top, right, bottom) to the tracker
    # see the EyeLink Installation Guide, "Customizing Screen Settings"
    el_coords = "screen_pixel_coords = 0 0 %d %d" % (WIDTH - 1, HEIGHT - 1)
    el_tracker.sendCommand(el_coords)

    # Write a DISPLAY_COORDS message to the EDF file
    # Data Viewer needs this piece of info for proper visualization, see Data
    # Viewer User Manual, "Protocol for EyeLink Data to Viewer Integration"
    dv_coords = "DISPLAY_COORDS  0 0 %d %d" % (WIDTH - 1, HEIGHT - 1)
    el_tracker.sendMessage(dv_coords)

    # Configure a graphics environment (genv) for tracker calibration
    genv = CalibrationGraphics(el_tracker, hrl.graphics.screen)


    # Set background and foreground colors
    # parameters: foreground_color, background_color
    foreground_color = (0, 0, 0)
    background_color = (int(255*bg_blank), int(255*bg_blank), int(255*bg_blank))
    genv.setCalibrationColors(foreground_color, background_color)

    # Set up the calibration target
    #
    # The target could be a "circle" (default) or a "picture",
    # To configure the type of calibration target, set
    # genv.setTargetType to "circle", "picture", e.g.,
    # genv.setTargetType('picture')
    #
    # Use gen.setPictureTarget() to set a "picture" target, e.g.,
    # genv.setPictureTarget(os.path.join('images', 'fixTarget.bmp'))

    # Use a picture as the calibration target
    genv.setTargetType('picture')
    genv.setPictureTarget('fixTarget.bmp')

    # Configure the size of the calibration target (in pixels)
    # genv.setTargetSize(24)

    # Beeps to play during calibration, validation and drift correction
    # parameters: target, good, error
    #     target -- sound to play when target moves
    #     good -- sound to play on successful operation
    #     error -- sound to play on failure or interruption
    # Each parameter could be ''--default sound, 'off'--no sound, or a wav file
    # e.g., genv.setCalibrationSounds('type.wav', 'qbeep.wav', 'error.wav')
    genv.setCalibrationSounds('', '', '')

    # Request Pylink to use the Pygame window we opened above for calibration
    pylink.openGraphicsEx(genv)

    ###########################################################################   
    # #Iterate across all blocks that need to be presented
    for i in range(len(blockstorun['number'])):

        ########## Calibrating eyetracker before every block  #################   
        # skip this step if running the script in Dummy Mode
        if not dummy_mode:
            try:
                el_tracker.doTrackerSetup()
            except RuntimeError as err:
                print('ERROR:', err)
                el_tracker.exitCalibration()

        ###########################################################################    

        sess = int(blockstorun['number'][i])
        print(sess)
        bl = blockstorun['block'][i]

        print("Block %d " % sess)

        start_trl = get_last_trial(vp_id, sess)


        # log file name and location
        design = read_design_csv('design/%s/block_%d.csv' %(vp_id, sess))
        rfl    = open('results/%s/block_%d.csv' % (vp_id, sess), 'a')

        #  get end trial
        end_trl   = len(design['Trial'])


        if start_trl == 0:
            result_headers = ['block', 'trial', 'alpha1', 'alpha2', 'tau1', 'tau2', 'Response', 'resp.time', 'timestamp']
            rfl.write(','.join(result_headers)+'\n')


        # loop over one block
        # ================
        for trl in np.arange(start_trl, end_trl):
            run_trial(hrl, trl, sess,  start_trl, end_trl) # function that executes the experiment

        # close result file for this block
        rfl.close()

        # save the block just done
        if trl==(end_trl-1):
            bfl.write('%d,%s\n' %(sess, bl))
            bfl.flush()


        # continue?
        if i < len(blockstorun['number']) - 1 :
            btn = show_continue(hrl, i+1, len(blockstorun['number']))
            print("continue screen, pressed ", btn)
            if btn == 'Left':
                break


    # close block done file
    bfl.close()

    # finishes everything
    hrl.close()
    print("Session exited")


# EOF
