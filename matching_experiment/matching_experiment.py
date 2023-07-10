#!/usr/bin/env python
"""
Asymmetric matching experiment with external, variegatd matching field

Uses HRL on python 3


@authors: CW, GA.
"""


import time
from socket import gethostname

import experiment_logic
import text_displays
from helper_functions import read_design_csv
from hrl import HRL

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
    for trial_idx in range(start_trial, end_trial):
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
        trial_result = experiment_logic.run_trial(ihrl, **trial_design)
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
