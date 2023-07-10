#!/usr/bin/env python
"""
Asymmetric matching experiment with external, variegatd matching field

Uses HRL on python 3


@authors: CW, GA.
"""


import time
from socket import gethostname

import data_management
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
        rfl = open(f"../data/results/{vp_id}/{vp_id}.txt")
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


def experiment_main(ihrl):
    participant = data_management.participant

    # get last trial from results file, to be able to resume from that trial onwards
    start_trial = get_last_trial(participant)

    # read design file and open result file for saving
    design = read_design_csv(f"../data/design/{participant}/{participant}.csv")

    #  get last trial (total number of trials)
    end_trial = len(design["Trial"])

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
        trial = {
            "participant": participant,
            "context": design["context"][trial_idx],
            "r": float(design["r"][trial_idx]),
            "Trial": int(design["Trial"][trial_idx]),
        }

        # Run trial
        trial_result = experiment_logic.run_trial(ihrl, **trial)
        trial_result["stop_time"] = time.time()
        trial.update(trial_result)

        # Save trial
        data_management.save_trial(trial, block_id="0")

    print("Session complete")


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
