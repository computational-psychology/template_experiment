import data_management
import numpy as np
import pandas as pd
import stimuli

luminances = [0, 0.25, 0.75, 1]

stim_names = stimuli.__all__


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
