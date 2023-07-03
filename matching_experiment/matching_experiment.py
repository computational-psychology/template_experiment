#!/usr/bin/env python
"""
Asymmetric matching experiment with external, variegatd matching field

Uses HRL on python 3


@authors: CW, GA.
"""

import random
import sys
import time
from socket import gethostname

import adjustment
import numpy as np
import text_displays

### Imports ###
from helper_functions import image_to_array, read_design_csv
from hrl import HRL
from hrl.graphics import graphics
from make_comp_surround import make_life_matches

inlab_siemens = True if "vlab" in gethostname() else False
inlab_viewpixx = True if "viewpixx" in gethostname() else False

if inlab_siemens:
    # size of Siements monitor
    WIDTH = 1024
    HEIGHT = 768
    bg_blank = 0.1  # corresponding to 50 cd/m2 approx

elif inlab_viewpixx:
    # size of VPixx monitor
    WIDTH = 1920
    HEIGHT = 1080
    bg_blank = 0.27  # corresponding to 50 cd/m2 approx

else:
    WIDTH = 1024
    HEIGHT = 768
    bg_blank = 0.27

# center of screen
whlf = WIDTH / 2.0
hhlf = HEIGHT / 2.0


# big and small steps during adjustment
STEP_SIZES = (0.02, 0.002)


## Functions which are needed for the experiment
def show_stimulus(hrl, checkerboard, curr_match, match_lum):
    # draw the checkerboard
    checkerboard.draw((whlf - checkerboard.wdth / 2, hhlf - checkerboard.hght / 2))
    # print "new_match_lum =", match_lum

    # create match stimulus with adjusted luminance
    center_display = show_match(hrl, match_lum, curr_match)
    center_display.draw((whlf - center_display.wdth / 2, hhlf / 4 - 50))

    # flip everything
    hrl.graphics.flip(clr=False)  # clr= True to clear buffer

    # delete texture from buffer
    # graphics.deleteTextureDL(center_display._dlid)


def adjust_loop(hrl, match_lum, checkerboard, curr_match):
    accept = False
    while not accept:
        match_lum, accept = adjustment.adjust(ihrl=hrl, value=match_lum, step_size=STEP_SIZES)
        show_stimulus(hrl, checkerboard, curr_match, match_lum)

    print("MatchLum =", match_lum)

    return match_lum


def show_match(hrl, match_lum, curr_match):
    # replace the center patch on top of the match_display
    # and adjust it to the matched luminace

    center = np.copy(curr_match)
    center[center < 0] = match_lum
    # create new texture
    center_display = hrl.graphics.newTexture(center)
    return center_display


def match_stimulus(trl):
    trial_match, all_surround = make_life_matches(trl)
    # return the one with a -1 at the center patch, so we can easily replace this area later on
    # print all_surround
    return trial_match[-1], all_surround


def get_last_trial(vp_id):
    try:
        rfl = open(f"results/{vp_id}/{vp_id}.txt")
    except OSError:
        print("result file not found")
        return 0

    for line in rfl:
        try:
            last_trl = int(line.split("\t")[0])
        except ValueError:
            pass

    if last_trl > 0:
        last_trl = last_trl + 1

    return last_trl


def run_trial(hrl, trl, start_trl, end_trl):
    # function written by Torsten and edited by Christiane, reused by GA
    # read out variable values for each trial from the design matrix
    print("TRIAL =", trl)

    # show break automatically, define after how many trials
    if trl > 0 and (trl - start_trl) == (end_trl - start_trl) // 2:
        text_displays.block_break(hrl, trial=(trl - start_trl), total_trials=(end_trl - start_trl))

    # get values from design matrix for current trial
    context, r, Trial = design["context"][trl], float(design["r"][trl]), int(design["Trial"][trl])

    # use these variable values to define test stimulus (name corresponds to design matrix and name of saved image)
    stim_name = f"stimuli/{vp_id}/{Trial}_{context}_{r:.2f}"

    # print "r =", r

    # load stimlus image and convert from png to numpy array
    curr_image = image_to_array(stim_name)

    # texture creation in buffer : stimulus
    checkerboard = hrl.graphics.newTexture(curr_image)

    # generate match stimulus
    trial_match, all_surround = match_stimulus(trl)

    t1 = time.time()

    # curr_match = np.array(trial_match.shape, dtype=np.float64)
    curr_match = trial_match / 255.0
    # print curr_match[60]

    # starting intensity of matching field: random between 0 and 1
    match_intensity_start = random.random()

    # Show stimulus and match
    show_stimulus(hrl, checkerboard, curr_match, match_intensity_start)

    # adjust the lumiance
    match_intensity = adjust_loop(hrl, match_intensity_start, checkerboard, curr_match)

    t2 = time.time()
    resptime = t2 - t1
    timestamp = time.time()

    rfl.write(
        "%d\t%s\t%s\t%f\t%f\t%f\t%f\t%f\n"
        % (
            Trial,
            context,
            stim_name,
            r,
            match_intensity_start,
            match_intensity,
            resptime,
            timestamp,
        )
    )
    rfl.flush()

    # surround information of matching patch should be written together with matched value
    fid_all_match.write(
        "%d\t%d\t%d\t%d\t%d\t%d\t%d\t%d\t%d\t%d\t%d\t%d\t%d\t%d\t%d\t%d\t%d\t%d\t%d\t%d\t%d\t%d\t%d\t%d\n"
        % (
            all_surround[0, 0],
            all_surround[0, 1],
            all_surround[0, 2],
            all_surround[0, 3],
            all_surround[0, 4],
            all_surround[1, 0],
            all_surround[1, 1],
            all_surround[1, 2],
            all_surround[1, 3],
            all_surround[1, 4],
            all_surround[2, 0],
            all_surround[2, 1],
            all_surround[2, 3],
            all_surround[2, 4],
            all_surround[3, 0],
            all_surround[3, 1],
            all_surround[3, 2],
            all_surround[3, 3],
            all_surround[3, 4],
            all_surround[4, 0],
            all_surround[4, 1],
            all_surround[4, 2],
            all_surround[4, 3],
            all_surround[4, 4],
        )
    )
    fid_all_match.flush()

    # screenshooting
    # gl.glReadBuffer(gl.GL_FRONT)
    # pixels = gl.glReadPixels(0,0, WIDTH, HEIGHT, gl.GL_RGB, gl.GL_UNSIGNED_BYTE)

    # image = Image.fromstring("RGB", (WIDTH, HEIGHT), pixels)
    # image = image.transpose( Image.FLIP_TOP_BOTTOM)
    # image.save('screenshot_%d.png' % trl)

    # clean checkerboard texture
    graphics.deleteTextureDL(checkerboard._dlid)

    return match_intensity


### Run Main ###
if __name__ == "__main__":
    LANG = "en"  # 'de' or 'en'

    vp_id = input("Bitte geben Sie Ihre Initialen ein (z.B. demo): ")

    # get last trial from results file, to be able to resume from that trial onwards
    start_trl = get_last_trial(vp_id)

    # read design file and open result file for saving
    design = read_design_csv(f"design/{vp_id}/{vp_id}.csv")

    #  get last trial (total number of trials)
    end_trl = len(design["Trial"])

    # results file
    rfl = open(f"results/{vp_id}/{vp_id}.txt", "a")

    # file to save surround of match check
    fid_all_match = open(f"results/{vp_id}/{vp_id}_all_match_surr.txt", "a")

    if start_trl == 0:
        # fid_match.write('b2\tc2\td2\td3\td4\tc4\tb4\tb3\n')
        result_headers = [
            "trial",
            "context",
            "image.fname",
            "r",
            "start_idx",
            "match_lum",
            "resp.time",
            "timestamp",
        ]
        rfl.write("\t".join(result_headers) + "\n")

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
            lut="lut.csv",
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
            lut="lut_viewpixx.csv",
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

    # loop over trials in design file
    # ================================
    for trl in np.arange(start_trl, end_trl):
        run_trial(hrl, trl, start_trl, end_trl)  # function that executes the experiment

    hrl.close()
    print("Session complete")
    rfl.close()
