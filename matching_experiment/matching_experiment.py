#!/usr/bin/env python
"""
Asymmetric matching experiment with external, variegatd matching field

Uses HRL on python 3


@authors: CW, GA.
"""

import random
import time
from socket import gethostname

import adjustment
import numpy as np
import text_displays
from asymmetric_matching import matching_field, perturb_array
from helper_functions import image_to_array, read_design_csv
from hrl import HRL
from stimuli import show_stimulus

inlab_siemens = "vlab" in gethostname()
inlab_viewpixx = "viewpixx" in gethostname()

if inlab_siemens:
    SETUP = {
        "graphics": "datapixx",
        "inputs": "responsepixx",
        "scrn": 1,
        "lut": "lut.csv",
        "fs": True,
    }
    # size of Siemens monitor
    WIDTH = 1024
    HEIGHT = 768
    bg_blank = 0.1  # corresponding to 50 cd/m2 approx

elif inlab_viewpixx:
    SETUP = {
        "graphics": "viewpixx",
        "inputs": "responsepixx",
        "scrn": 1,
        "lut": "lut_viewpixx.csv",
        "fs": True,
    }
    # size of VPixx monitor
    WIDTH = 1920
    HEIGHT = 1080
    bg_blank = 0.27  # corresponding to 50 cd/m2 approx

else:
    SETUP = {
        "graphics": "gpu",
        "inputs": "keyboard",
        "scrn": 0,
        "lut": None,
        "fs": True,
    }
    WIDTH = 1024
    HEIGHT = 768
    bg_blank = 0.27

PPD = 32

# big and small steps during adjustment
STEP_SIZES = (0.02, 0.002)

VARIEGATED_ARRAY = np.loadtxt("matchsurround.txt")


def adjust_loop(ihrl, match_intensity, stimulus_texture, matching_field_stim):
    accept = False
    while not accept:
        match_intensity, accept = adjustment.adjust(
            ihrl=ihrl, value=match_intensity, step_size=STEP_SIZES
        )
        show_stimulus(
            ihrl=ihrl,
            stimulus_texture=stimulus_texture,
            matching_field_stim=matching_field_stim,
            match_intensity=match_intensity,
        )

    print(f"Match intensity = {match_intensity}")

    return match_intensity


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
            last_trl = 0

    if last_trl > 0:
        last_trl = last_trl + 1

    return last_trl


def save_trial(
    Trial,
    context,
    stim_name,
    r,
    match_intensity_start,
    match_intensity,
    resptime,
    stop_time,
    participant,
):
    with open(f"results/{participant}/{participant}.txt", "a") as rfl:
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
                stop_time,
            )
        )


def save_variegated(variegated_array, participant):
    # surround information of matching patch should be written together with matched value
    with open(f"results/{participant}/{participant}_all_match_surr.txt", "a") as fid_all_match:
        fid_all_match.write(
            "%d\t%d\t%d\t%d\t%d\t%d\t%d\t%d\t%d\t%d\t%d\t%d\t%d\t%d\t%d\t%d\t%d\t%d\t%d\t%d\t%d\t%d\t%d\t%d\n"
            % (
                variegated_array[0, 0],
                variegated_array[0, 1],
                variegated_array[0, 2],
                variegated_array[0, 3],
                variegated_array[0, 4],
                variegated_array[1, 0],
                variegated_array[1, 1],
                variegated_array[1, 2],
                variegated_array[1, 3],
                variegated_array[1, 4],
                variegated_array[2, 0],
                variegated_array[2, 1],
                variegated_array[2, 3],
                variegated_array[2, 4],
                variegated_array[3, 0],
                variegated_array[3, 1],
                variegated_array[3, 2],
                variegated_array[3, 3],
                variegated_array[3, 4],
                variegated_array[4, 0],
                variegated_array[4, 1],
                variegated_array[4, 2],
                variegated_array[4, 3],
                variegated_array[4, 4],
            )
        )

    # screenshooting
    # gl.glReadBuffer(gl.GL_FRONT)
    # pixels = gl.glReadPixels(0,0, WIDTH, HEIGHT, gl.GL_RGB, gl.GL_UNSIGNED_BYTE)

    # image = Image.fromstring("RGB", (WIDTH, HEIGHT), pixels)
    # image = image.transpose( Image.FLIP_TOP_BOTTOM)
    # image.save('screenshot_%d.png' % trl)


def run_trial(ihrl, context, r, Trial, participant):
    # function written by Torsten and edited by Christiane, reused by GA

    # use these variable values to define test stimulus (name corresponds to design matrix and name of saved image)
    stim_name = f"stimuli/{participant}/{Trial}_{context}_{r:.2f}"

    # load stimlus image and convert from png to numpy array
    stimulus_image = image_to_array(stim_name)

    # texture creation in buffer : stimulus
    checkerboard_stimulus = ihrl.graphics.newTexture(stimulus_image)

    # starting intensity of matching field: random between 0 and 1
    match_intensity_start = random.random()

    # create matching field (variegated checkerboard)
    variegated_array = perturb_array(VARIEGATED_ARRAY, seed=Trial)

    matching_field_stim = matching_field(
        variegated_array=variegated_array,
        ppd=PPD,
        field_size=(1, 1),
        field_intensity=match_intensity_start,
        check_visual_size=(0.5, 0.5),
    )

    # Show stimulus (and matching field)
    t1 = time.time()
    show_stimulus(
        ihrl,
        stimulus_texture=checkerboard_stimulus,
        matching_field_stim=matching_field_stim,
        match_intensity=match_intensity_start,
    )

    # adjust the matching field intensity
    match_intensity = adjust_loop(
        ihrl,
        stimulus_texture=checkerboard_stimulus,
        matching_field_stim=matching_field_stim,
        match_intensity=match_intensity_start,
    )

    # Record response time
    t2 = time.time()
    resptime = t2 - t1

    # Save variegated array
    save_variegated(variegated_array, participant=participant)

    # clean checkerboard texture
    checkerboard_stimulus.delete()

    return {
        "match_intensity": match_intensity,
        "match_intensity_start": match_intensity_start,
        "stim_name": stim_name,
        "resptime": resptime,
    }


def experiment_main(ihrl):
    participant = input("Bitte geben Sie Ihre Initialen ein (z.B. demo): ")

    # get last trial from results file, to be able to resume from that trial onwards
    start_trial = get_last_trial(participant)

    # read design file and open result file for saving
    design = read_design_csv(f"design/{participant}/{participant}.csv")

    #  get last trial (total number of trials)
    end_trial = len(design["Trial"])

    if start_trial == 0:
        with open(f"results/{participant}/{participant}.txt", "a") as rfl:
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

    # loop over trials in design file
    # ================================
    for trial_idx in np.arange(start_trial, end_trial):
        print(f"TRIAL {trial_idx}: ")

        # show break automatically, define after how many trials
        if trial_idx > 0 and (trial_idx - start_trial) == (end_trial - start_trial) // 2:
            text_displays.block_break(
                ihrl, trial=(trial_idx - start_trial), total_trials=(end_trial - start_trial)
            )

        # current trial design variables, as dict
        trial_design = {
            "participant": participant,
            "context": design["context"][trial_idx],
            "r": float(design["r"][trial_idx]),
            "Trial": int(design["Trial"][trial_idx]),
        }

        # Run trial
        trial_result = run_trial(ihrl, **trial_design)
        trial_result["stop_time"] = time.time()

        # Save trial
        save_trial(
            **trial_design,
            **trial_result,
        )

    print("Session complete")
    rfl.close()


if __name__ == "__main__":
    LANG = "en"  # 'de' or 'en'

    # Create HRL interface object with parameters that depend on the setup
    ihrl = HRL(
        **SETUP,
        wdth=WIDTH,
        hght=HEIGHT,
        bg=bg_blank,
        photometer=None,
        db=True,
    )

    experiment_main(ihrl)

    ihrl.close()
