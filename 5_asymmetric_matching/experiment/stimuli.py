import copy

import numpy as np
import stimupy

resolution = {
    "visual_size": (10, 20),
    "ppd": 32,
}

target_size = resolution["visual_size"][1] / 10

intensity_background = 0.3

__all__ = ["whites"]


# # %% SBC
# def sbc(intensity_target, target_side):
#     return stimupy.stimuli.sbcs.two_sided(
#         **resolution,
#         target_size=target_size,
#         intensity_target=intensity_target,
#         intensity_backgrounds=(0.0, 1.0)
#     )


# %% WHITE'S
def whites(intensity_target, target_side):
    if target_side == "Left":
        intensities = (intensity_target, 1.0)
    elif target_side == "Right":
        intensities = (0.0, intensity_target)

    return stimupy.stimuli.whites.white(
        **resolution,
        bar_width=target_size,
        target_indices=(2, -3),
        target_heights=target_size,
        intensity_bars=(0.0, 1.0),
        intensity_target=intensities
    )


# %% MATCHING FIELD
def matching_field(intensity_match):
    # Generate checkerboard
    checkerboard = stimupy.checkerboards.checkerboard(
        board_shape=(5, 5), check_visual_size=(0.5, 0.5), ppd=resolution["ppd"]
    )

    # TODO: apply variegation

    # Overlay matching field
    field = stimupy.components.shapes.rectangle(
        visual_size=checkerboard["visual_size"],
        ppd=resolution["ppd"],
        rectangle_size=(1, 1),
        intensity_rectangle=intensity_match,
    )
    combined = copy.deepcopy(checkerboard)
    combined["field_mask"] = field["rectangle_mask"]
    combined["img"] = np.where(combined["field_mask"], field["img"], checkerboard["img"])
    return combined
