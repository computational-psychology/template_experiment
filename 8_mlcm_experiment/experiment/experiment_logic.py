import sys
import time

import numpy as np
import stimuli
import text_displays


def display_stim(
    ihrl,
    target_intensity_left,
    surround_intensity_left,
    target_intensity_right,
    surround_intensity_right,
):
    """Display stimulus for current trial"""

    stimulus_left = stimuli.sbc_circular(
        intensity_target=target_intensity_left,
        intensity_surround=surround_intensity_left,
        intensity_background=ihrl.graphics.background,
    )

    stimulus_right = stimuli.sbc_circular(
        intensity_target=target_intensity_right,
        intensity_surround=surround_intensity_right,
        intensity_background=ihrl.graphics.background,
    )

    ppd = stimuli.resolution["ppd"]

    # Convert the stimulus image(matrix) to an OpenGL texture
    stim_texture_left = ihrl.graphics.newTexture(stimulus_left["img"])
    stim_texture_right = ihrl.graphics.newTexture(stimulus_right["img"])

    # Determine position: we want the stimulus around the center
    center = (ihrl.width // 2, ihrl.height // 2)

    R = 4  # deg
    offset_x = int(ppd * R * 0.866)  # cos(30) = 0.866
    offset_y = 0

    pos_left = (
        center[0] - offset_x - (stim_texture_left.wdth // 2),
        center[1] + offset_y - (stim_texture_left.hght // 2),
    )

    pos_right = (
        center[0] + offset_x - (stim_texture_left.wdth // 2),
        center[1] + offset_y - (stim_texture_left.hght // 2),
    )

    # Draw textures on the frame buffer
    draw_fixation_cross(ihrl)

    # Draw SBCs
    stim_texture_left.draw(pos=pos_left, sz=(stim_texture_left.wdth, stim_texture_left.hght))
    stim_texture_right.draw(pos=pos_right, sz=(stim_texture_right.wdth, stim_texture_right.hght))

    # Display: flip the frame buffer
    ihrl.graphics.flip()  # flips the frame buffer to show everything

    return


def draw_fixation_cross(ihrl):
    # draws fixation dot in the middle
    # TODO: use stimupy to actually draw a cross and not a square.
    fix = ihrl.graphics.newTexture(np.ones((5, 5)) * 0.0)
    fix.draw((ihrl.width // 2, ihrl.height // 2))


def display_fixation_cross(ihrl):
    ihrl.graphics.flip(clr=True)
    draw_fixation_cross(ihrl)
    ihrl.graphics.flip()

    return


def run_trial(
    ihrl,
    target_intensity_left,
    surround_intensity_left,
    target_intensity_right,
    surround_intensity_right,
    **kwargs
):
    """Function that runs sequence of events during one trial"""

    # Fixation cross
    display_fixation_cross(ihrl)

    # sleeps for 250 ms # using system time (inaccurate)
    time.sleep(0.25)

    # Display stimuli
    display_stim(
        ihrl,
        target_intensity_left=target_intensity_left,
        surround_intensity_left=surround_intensity_left,
        target_intensity_right=target_intensity_right,
        surround_intensity_right=surround_intensity_right,
    )

    # Wait for answer
    btn, t1 = ihrl.inputs.readButton(btns=["Left", "Right", "Escape", "Space"])

    # Raise SystemExit Exception
    if (btn == "Escape") or (btn == "Space"):
        sys.exit("Participant terminated experiment.")

    # end trial
    return {"response": btn, "resp.time": t1}


def display_instructions(ihrl):
    """Display instructions to the participant

    Parameters
    ----------
    ihrl : hrl-object
        hrl-interface object to use for display
    """
    lines = [
        "Paired comparisons task",
        "Please select the stimulus that is",
        "BRIGHTER",
        "Press either:",
        "LEFT or RIGHT",
        "",
        "Press MIDDLE button to start",
    ]

    text_displays.display_text(
        ihrl=ihrl, text=lines, intensity_background=ihrl.graphics.background
    )

    return
