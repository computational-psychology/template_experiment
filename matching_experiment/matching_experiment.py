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


def show_stimulus(hrl, stimulus_img, matching_field_img, match_intensity):
    # draw the checkerboard
    stimulus_img.draw((whlf - stimulus_img.wdth / 2, hhlf - stimulus_img.hght / 2))

    # create matching field with adjusted luminance
    matching_display = show_match(hrl, match_intensity, matching_field_img)
    matching_display.draw((whlf - matching_display.wdth / 2, hhlf / 4 - 50))

    # flip everything
    hrl.graphics.flip(clr=False)  # clr= True to clear buffer

    # delete texture from buffer
    # graphics.deleteTextureDL(center_display._dlid)


def show_match(hrl, match_intensity, matching_field_img):
    # replace the center patch on top of the match_display
    # and adjust it to the matched luminace

    center = np.copy(matching_field_img)
    center[center < 0] = match_intensity
    # create new texture
    center_display = hrl.graphics.newTexture(center)
    return center_display


def adjust_loop(hrl, match_intensity, stimulus_img, matching_field_img):
    accept = False
    while not accept:
        match_intensity, accept = adjustment.adjust(
            ihrl=hrl, value=match_intensity, step_size=STEP_SIZES
        )
        show_stimulus(
            hrl=hrl,
            stimulus_img=stimulus_img,
            matching_field_img=matching_field_img,
            match_intensity=match_intensity,
        )

    print(f"Match intensity = {match_intensity}")

    return match_intensity


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


def run_trial(hrl, trial_idx, start_trial, end_trial):
    # function written by Torsten and edited by Christiane, reused by GA
    # read out variable values for each trial from the design matrix
    print(f"TRIAL {trial_idx}: ")

    # show break automatically, define after how many trials
    if trial_idx > 0 and (trial_idx - start_trial) == (end_trial - start_trial) // 2:
        text_displays.block_break(
            hrl, trial=(trial_idx - start_trial), total_trials=(end_trial - start_trial)
        )

    # get values from design matrix for current trial
    context, r, Trial = (
        design["context"][trial_idx],
        float(design["r"][trial_idx]),
        int(design["Trial"][trial_idx]),
    )

    # use these variable values to define test stimulus (name corresponds to design matrix and name of saved image)
    stim_name = f"stimuli/{participant}/{Trial}_{context}_{r:.2f}"

    # load stimlus image and convert from png to numpy array
    stimulus_image = image_to_array(stim_name)

    # texture creation in buffer : stimulus
    checkerboard_stimulus = hrl.graphics.newTexture(stimulus_image)

    # Generate matching field
    trial_match, all_surround = match_stimulus(trial_idx)
    matching_field = trial_match / 255.0

    # starting intensity of matching field: random between 0 and 1
    match_intensity_start = random.random()

    # Show stimulus (and matching field)
    t1 = time.time()
    show_stimulus(hrl, checkerboard_stimulus, matching_field, match_intensity_start)

    # adjust the matching field intensity
    match_intensity = adjust_loop(
        hrl, match_intensity_start, checkerboard_stimulus, matching_field
    )
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
    graphics.deleteTextureDL(checkerboard_stimulus._dlid)

    return match_intensity


### Run Main ###
if __name__ == "__main__":
    LANG = "en"  # 'de' or 'en'

    participant = input("Bitte geben Sie Ihre Initialen ein (z.B. demo): ")

    # get last trial from results file, to be able to resume from that trial onwards
    start_trl = get_last_trial(participant)

    # read design file and open result file for saving
    design = read_design_csv(f"design/{participant}/{participant}.csv")

    #  get last trial (total number of trials)
    end_trl = len(design["Trial"])

    # results file
    rfl = open(f"results/{participant}/{participant}.txt", "a")

    # file to save surround of match check
    fid_all_match = open(f"results/{participant}/{participant}_all_match_surr.txt", "a")

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
