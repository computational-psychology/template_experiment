import data_management
import numpy as np
import pandas as pd
import stimuli
from adjustment import adjust

LUMINANCES = (0.5,)
SIDES = ("Left", "Right")

stim_names = stimuli.__all__

rng = np.random.default_rng()

# Define window parameters
SHAPE = (768, 1024)  # Desired shape of the drawing window
CENTER = (SHAPE[0] // 2, SHAPE[1] // 2)  # Center of the drawing window


def display_stim(ihrl, intensity_target, target_side, intensity_match):
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
    stimulus = stimuli.whites(intensity_target=intensity_target, target_side=target_side)

    # Convert the stimulus image(matrix) to an OpenGL texture
    stim_texture = ihrl.graphics.newTexture(stimulus["img"])

    # Determine position: we want the stimulus in the center of the frame
    pos = (CENTER[1] - (stim_texture.wdth // 2), CENTER[0] - (stim_texture.hght // 2))

    # Create a display: draw texture on the frame buffer
    stim_texture.draw(pos=pos, sz=(stim_texture.wdth, stim_texture.hght))

    # Draw matching field
    draw_match(ihrl, intensity_match=intensity_match)

    # Display: flip the frame buffer
    ihrl.graphics.flip(clr=True)  # also `clear` the frame buffer

    return


def draw_match(ihrl, intensity_match):
    stim = stimuli.matching_field(intensity_match=intensity_match)
    stim_texture = ihrl.graphics.newTexture(stim["img"])
    pos = (CENTER[1] - (stim_texture.wdth // 2), 0.6 * (stim_texture.hght))

    # Create a display: draw texture on the frame buffer
    stim_texture.draw(pos=pos, sz=(stim_texture.wdth, stim_texture.hght))


def run_trial(ihrl, intensity_target, target_side, **kwargs):
    # Pick random starting intensity for matching field
    intensity_match = rng.random()

    # Run adjustment
    accept = False
    while not accept:
        display_stim(
            ihrl,
            intensity_target=intensity_target,
            target_side=target_side,
            intensity_match=intensity_match,
        )
        intensity_match, accept = adjust(ihrl, value=intensity_match)

    return {"intensity_match": intensity_match}


def generate_session(Nrepeats=2):
    for i in range(Nrepeats):
        for stim_name in stim_names:
            block = generate_block(stim_name)
            block_id = f"matching-{stim_name}-{i}"

            # Save to file
            filepath = data_management.design_filepath(block_id)
            block.to_csv(filepath)


def generate_block(stim_name):
    # Combine all variables into full design
    trials = [(stim_name, int_target, side) for int_target in LUMINANCES for side in SIDES]

    # Convert to dataframe
    block = pd.DataFrame(
        trials,
        columns=["stim", "intensity_target", "target_side"],
    )

    # Shuffle trial order
    block = block.reindex(np.random.permutation(block.index))
    block.reset_index(drop=True, inplace=True)
    block.index.name = "trial"

    return block
