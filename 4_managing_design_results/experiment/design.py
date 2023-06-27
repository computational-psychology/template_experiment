"""This module defines the actual experimental design of [this] experiment.

It needs to _at least_ define these functions, which are called by `run_experiment.py`
- run_trial: how to run a single trial of this experiment
- generate_session: how to generate a new session's worth of design (files)

It can define additional functions to help manage the control flow.

"""

import sys

import data_management
import numpy as np
import pandas as pd
import stimuli

luminances = [0, 0.25, 0.75, 1]

stim_names = stimuli.__all__


# Define window parameters
SHAPE = (1024, 1024)  # Desired shape of the drawing window
CENTER = (SHAPE[0] // 2, SHAPE[1] // 2)  # Center of the drawing window


def display_stim(ihrl, stim, intensity_target, intensity_left, intensity_right):
    """Display stimulus with specified target, context intensities

    Parameters
    ----------
    ihrl : hrl-object
        hrl-interface object to use for display
    stim : str
        which stimulus to display, "sbc" or "whites"
    intensity_target : float
        intensity value for the targets
    intensity_left : float
        intensity value for the left context
    intensity_right : float
        intensity value for the right context
    """
    if stim == "sbc":
        stimulus = stimuli.sbc(intensity_target, intensity_left, intensity_right)
    elif stim == "whites":
        stimulus = stimuli.whites(intensity_target, intensity_left, intensity_right)

    # Convert the stimulus image(matrix) to an OpenGL texture
    stim_texture = ihrl.graphics.newTexture(stimulus["img"])

    # Determine position: we want the stimulus in the center of the frame
    pos = (CENTER[1] - (stim_texture.wdth // 2), CENTER[0] - (stim_texture.hght // 2))

    # Create a display: draw texture on the frame buffer
    stim_texture.draw(pos=pos, sz=(stim_texture.wdth, stim_texture.hght))

    # Display: flip the frame buffer
    ihrl.graphics.flip(clr=True)  # also `clear` the frame buffer

    return


def respond(ihrl):
    press, _ = ihrl.inputs.readButton(btns=("Left", "Right", "Escape", "Space"))

    if press in ("Escape", "Space"):
        # Raise SystemExit Exception
        sys.exit("Participant terminated experiment.")
    else:
        return press


def run_trial(ihrl, stim, intensity_target, intensity_left, intensity_right, **kwargs):
    """Run single trial of this experiment

    This function defines the structure and procedure for a single trial in this experiment.

    Parameters
    ----------
    ihrl : hrl-object
        hrl-interface object to use for display
    stim : str
        which stimulus to display, "sbc" or "whites"
    intensity_target : float
        intensity value for the targets
    intensity_left : float
        intensity value for the left context
    intensity_right : float
        intensity value for the right context

    Returns
    -------
    dict(str: Any)
        trail results: raw resonse, and converted/processed result.
        Will be added to the trial dict, before saving.
    """
    display_stim(ihrl, stim, intensity_target, intensity_left, intensity_right)
    response = respond(ihrl)

    if response == "Left":
        result = intensity_left
    elif response == "Right":
        result = intensity_right

    return {"response": response, "result": result}


def generate_session(Nrepeats=2):
    for i in range(Nrepeats):
        for stim_name in stim_names:
            block = generate_block(stim_name)
            block_id = f"{stim_name}-{i}"

            # Save to file
            filepath = data_management.design_filepath(block_id)
            block.to_csv(filepath)


def generate_block(stim_name):
    # Combine all variables into full design
    trials = [
        (stim_name, int_target, int_left, int_right)
        for int_target in luminances
        for int_left in luminances
        for int_right in luminances
    ]

    # Convert to dataframe
    block = pd.DataFrame(
        trials,
        columns=["stim", "intensity_target", "intensity_left", "intensity_right"],
    )

    # Shuffle trial order
    block = block.reindex(np.random.permutation(block.index))
    block.reset_index(drop=True, inplace=True)
    block.index.name = "trial"

    return block
