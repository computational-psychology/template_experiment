import sys

from hrl import HRL
from stimuli import stims

# ------------------------------------- #
#              0. SETUP                 #
# ------------------------------------- #
# Define window parameters
SHAPE = (1024, 1024)  # Desired shape of the drawing window
CENTER = (SHAPE[0] // 2, SHAPE[1] // 2)  # Center of the drawing window


# ------------------------------------- #
#               2. DISPLAY              #
# ------------------------------------- #
def display_stim(ihrl, stim_image):
    """
    In this "experiment", we just display a collection of stimuli, one at a time.
    Here we define a function to display a single stimulus image centrally on the screen.
    """

    # Convert the stimulus image(matrix) to an OpenGL texture
    stim_texture = ihrl.graphics.newTexture(stim_image)

    # Determine position: we want the stimulus in the center of the frame
    pos = (CENTER[1] - (stim_texture.wdth // 2), CENTER[0] - (stim_texture.hght // 2))

    # Create a display: draw texture on the frame buffer
    stim_texture.draw(pos=pos, sz=(stim_texture.wdth, stim_texture.hght))

    # Display: flip the frame buffer
    ihrl.graphics.flip(clr=True)  # also `clear` the frame buffer

    return


# ------------------------------------- #
#    3&4. CAPTURE & PROCESS RESPONSE    #
# ------------------------------------- #
def select_stim(ihrl, stim_idx, max_idx):
    """
    We'll use the Left/Right keys to go through the list of stimuli,
    and the Escape/Space keys to terminate.

    Here we define a function that captures and processes responses.
    On Escape/Space, it raises a SystemExit exception to terminate.
    On Left/Right, it decreases/increases (resp.) the index
    into the list of stimuli by 1.
    To prevent IndexErrors, make sure that the index cannot be <0 or >max
    """

    press, _ = ihrl.inputs.readButton(btns=("Left", "Right", "Escape", "Space"))

    if press in ("Escape", "Space"):
        # Raise SystemExit Exception
        sys.exit("Participant terminated experiment.")
    elif press == "Left":
        stim_idx -= 1
        stim_idx = max(stim_idx, 0)
    elif press == "Right":
        stim_idx += 1
        stim_idx = min(stim_idx, max_idx)

    return stim_idx


# ------------------------------------- #
#           MAIN EXPERIMENT LOOP        #
# ------------------------------------- #


def experiment_main(ihrl):
    stim_names = [*stims.keys()]
    print(f"Stimuli avialable: {stim_names}")

    stim_idx = 0
    while True:
        """Define stimuli
        We have extracted / modularized the stimulus definitions
        to stimuli.py, where all stimuli are generated into a dict called `stims`
        --  which we imported earlier.
        """

        # Main loop
        try:
            # Display stimulus
            stim_name = stim_names[stim_idx]
            print(f"Showing {stim_name}")
            stim = stims[stim_name]
            stim_image = stim["img"]
            display_stim(ihrl, stim_image)

            # Select next stim
            stim_idx = select_stim(ihrl, stim_idx, max_idx=len(stim_names) - 1)
        except SystemExit as e:
            # Cleanup
            print("Exiting...")
            ihrl.close()
            raise e


if __name__ == "__main__":
    # Create HRL interface object
    ihrl = HRL(
        graphics="gpu",  # Use the default GPU as graphics device driver
        # graphics='datapixx',    # In the lab, we use the datapixx device driver
        inputs="keyboard",  # Use the keyboard as input device driver
        # inputs="responsepixx",  # In the lab, we use the responsepixx input device
        hght=SHAPE[0],
        wdth=SHAPE[1],
        scrn=0,  # Which screen (monitor) to use
        fs=False,  # Fullscreen?
        bg=0.5,  # background intensity (black=0.0; white=1.0)
    )
    experiment_main(ihrl)
    ihrl.close()