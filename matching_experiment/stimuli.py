import numpy as np


def show_stimulus(
    ihrl,
    stimulus_texture,
    matching_field_stim,
    match_intensity,
):
    # Draw the stimulus
    stimulus_texture.draw(
        (
            (ihrl.width // 2) - stimulus_texture.wdth / 2,
            (ihrl.height // 2) - stimulus_texture.hght / 2,
        )
    )

    # Update matching field intensity
    matching_field_stim["img"] = np.where(matching_field_stim["field_mask"], match_intensity, matching_field_stim["img"])

    # Draw the matching field
    matching_texture = ihrl.graphics.newTexture(matching_field_stim["img"])
    matching_texture.draw(
        ((ihrl.width // 2) - matching_texture.wdth / 2, ((ihrl.height // 2)) / 4 - 50)
    )

    # flip everything
    ihrl.graphics.flip(clr=False)  # clr= True to clear buffer
