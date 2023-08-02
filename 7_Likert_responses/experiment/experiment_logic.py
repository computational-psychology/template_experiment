import sys

import numpy as np

import stimuli
from text_displays import text_to_arr

stim_names = stimuli.stims.keys()

rng = np.random.default_rng()



def display_stim(ihrl, stim, response_position):
    """Display stimulus with specified target, context intensities

    Parameters
    ----------
    ihrl : hrl-object
        hrl-interface object to use for display
    stim : str
        which stimulus to display, "sbc" or "whites"
    intensity_target : float
        intensity value for the targets
    """
    stimulus = stimuli.stims[stim]

    # Convert the stimulus image(matrix) to an OpenGL texture
    stim_texture = ihrl.graphics.newTexture(stimulus["img"])

    # Determine position: we want the stimulus in the center of the frame
    window_center = (ihrl.height // 2, ihrl.width // 2)  # Center of the drawing window
    pos = (window_center[1] - (stim_texture.wdth // 2), window_center[0] - (stim_texture.hght // 2))

    # Create a display: draw texture on the frame buffer
    stim_texture.draw(pos=pos, sz=(stim_texture.wdth, stim_texture.hght))

    # Draw Likert-scale options
    draw_options(ihrl, response_position)

    # Display: flip the frame buffer
    ihrl.graphics.flip(clr=True)  # also `clear` the frame buffer


# %% DRAW LIKERT OPTIONS
def draw_options(ihrl, position):
    txt_ints = [0.0] * 5
    txt_ints[position - 1] = 1.0

    t1 = ihrl.graphics.newTexture(
        text_to_arr(
            "Left target is definitely brighter",
            intensity_background=ihrl.background,
            intensity_text=txt_ints[0],
            fontsize=25,
        ),
        "square",
    )
    t2 = ihrl.graphics.newTexture(
        text_to_arr(
            "Left target is maybe brighter",
            intensity_background=ihrl.background,
            intensity_text=txt_ints[1],
            fontsize=25,
        ),
        "square",
    )
    t3 = ihrl.graphics.newTexture(
        text_to_arr(
            "Targets are equally bright",
            intensity_background=ihrl.background,
            intensity_text=txt_ints[2],
            fontsize=25,
        ),
        "square",
    )
    t4 = ihrl.graphics.newTexture(
        text_to_arr(
            "Right target is maybe brighter",
            intensity_background=ihrl.background,
            intensity_text=txt_ints[3],
            fontsize=25,
        ),
        "square",
    )
    t5 = ihrl.graphics.newTexture(
        text_to_arr(
            "Right target is definitely brighter",
            intensity_background=ihrl.background,
            intensity_text=txt_ints[4],
            fontsize=25,
        ),
        "square",
    )

    t1.draw((102, 1010), (t1.wdth, t1.hght))
    t2.draw((102 + t1.wdth + 20, 1010), (t2.wdth, t2.hght))
    t3.draw((102 + t2.wdth + t1.wdth + 40, 1010), (t3.wdth, t3.hght))
    t4.draw((102 + t1.wdth + t2.wdth + t3.wdth + 60, 1010), (t4.wdth, t4.hght))
    t5.draw((102 + t1.wdth + t2.wdth + t3.wdth + t4.wdth + 80, 1010), (t5.wdth, t5.hght))


def select(ihrl, value, range):
    """Allow participant to select a value from a range of options

    Parameters
    ----------
    ihrl : hrl-object
        HRL-interface object to use for display
    value : int
        currently selected option
    range : (int, int)
        min and max values to select. If one value is given, assume min=0

    Returns
    -------
    int
        currently selected option
    bool
        whether this option was confirmed

    Raises
    ------
    SystemExit
        if participant/experimenter terminated by pressing Escape
    """
    try:
        len(range)
    except:
        range = (0, range)

    accept = False

    press, _ = ihrl.inputs.readButton(btns=("Left", "Right", "Escape", "Space"))

    if press == "Escape":
        # Raise SystemExit Exception
        sys.exit("Participant terminated experiment.")
    elif press == "Left":
        value -= 1
        value = max(value, range[0])
    elif press == "Right":
        value += 1
        value = min(value, range[1])
    elif press == "Space":
        accept = True

    return value, accept


def run_trial(ihrl, stim, **kwargs):
    response_position = 3

    # Run adjustment
    accept = False
    while not accept:
        display_stim(
            ihrl,
            stim,
            response_position=response_position,
        )
        response_position, accept = select(ihrl, value=response_position, range=(1, 5))

    return {"response": response_position}
