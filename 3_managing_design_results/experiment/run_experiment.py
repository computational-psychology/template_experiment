"""Run a session of [this] experiment

This module controls the basic experiment flow;
finding incomplete trails/blocks, and iterating through them.

The actual experimental procedure is defined in `design.py`

Raises
------
SystemExit
    if participant (/ experimenter) quits session before end
"""

import data_management
import design
import pandas as pd
import text_displays
from hrl import HRL


def run_block(hrl, block, block_id):
    print(f"Running block {block_id}")
    # Get start, end trial
    start_trl = block["trial"].iloc[0]
    end_trl = block["trial"].iloc[-1] + 1

    # loop over trials
    for idx, trial in block.iterrows():
        trial_id = trial["trial"]
        print(f"TRIAL {trial_id}")

        # show a break screen automatically after so many trials
        if (end_trl - trial_id) % (end_trl / 2) == 0 and (trial_id - start_trl) != 0:
            text_displays.block_break(ihrl, trial_id, (start_trl + (end_trl - start_trl)))

        # current trial design variables (convert from pandas row to dict)
        trial = trial.to_dict()

        # run trial
        t1 = pd.Timestamp.now().strftime("%Y%m%d:%H%M%S.%f")
        trial_results = design.run_trial(hrl, **trial)
        trial.update(trial_results)
        t2 = pd.Timestamp.now().strftime("%Y%m%d:%H%M%S.%f")

        # Record timing
        trial["start_time"] = t1
        trial["stop_time"] = t2

        # Save trial
        data_management.save_trial(trial, block_id)

    print(f"Block {block_id} all trials completed.")
    return block


def experiment_main(ihrl):
    # Get all blocks for this session
    incomplete_blocks = data_management.get_incomplete_blocks()
    if len(incomplete_blocks) == 0:
        # No existing blocks for this session. Generate.
        design.generate_session()
        incomplete_blocks = data_management.get_incomplete_blocks()
    print(f"{len(incomplete_blocks)} incomplete blocks")

    # Run
    try:
        # Iterate over all blocks that need to be presented
        for block_num, (block_id, block) in enumerate(incomplete_blocks.items()):
            # Run block
            print(f"Running session block {block_num+1}: {block_id}")
            block = run_block(ihrl, block=block, block_id=block_id)

            if block_num + 1 < len(incomplete_blocks):
                text_displays.block_end(ihrl, block_num + 1, len(incomplete_blocks))
    except SystemExit as e:
        # Cleanup
        print("Exiting...")
        ihrl.close()
        raise e

    # Close session
    ihrl.close()
    print("Session complete")


if __name__ == "__main__":
    # Create HRL interface object
    ihrl = HRL(
        graphics="gpu",  # Use the default GPU as graphics device driver
        # graphics='datapixx',    # In the lab, we use the datapixx device driver
        inputs="keyboard",  # Use the keyboard as input device driver
        # inputs="responsepixx",  # In the lab, we use the responsepixx input device
        hght=design.SHAPE[0],
        wdth=design.SHAPE[1],
        scrn=0,  # Which screen (monitor) to use
        fs=False,  # Fullscreen?
        bg=0.3,  # background intensity (black=0.0; white=1.0)
    )
    experiment_main(ihrl)
    ihrl.close()
