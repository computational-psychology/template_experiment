import numpy as np


def show_stimulus(ihrl, stimulus_texture, matching_field_img, match_intensity):
    # draw the checkerboard
    stimulus_texture.draw(
        (
            (ihrl.width // 2) - stimulus_texture.wdth / 2,
            (ihrl.height // 2) - stimulus_texture.hght / 2,
        )
    )

    # create matching field with adjusted luminance
    matching_display = show_match(ihrl, match_intensity, matching_field_img)
    matching_display.draw(
        ((ihrl.width // 2) - matching_display.wdth / 2, ((ihrl.height // 2)) / 4 - 50)
    )

    # flip everything
    ihrl.graphics.flip(clr=False)  # clr= True to clear buffer


def show_match(ihrl, match_intensity, matching_field_img):
    # replace the center patch on top of the match_display
    # and adjust it to the matched luminace

    center = np.copy(matching_field_img)
    center[center < 0] = match_intensity
    # create new texture
    center_display = ihrl.graphics.newTexture(center)
    return center_display
