import copy
import random
from pathlib import Path

import numpy as np
import stimupy
from PIL import Image
from stimupy.utils import array_to_image
from variegate import generate_variegated_array

INTENSITY_VALUES = np.array([5, 10, 17, 27, 42, 57, 75, 96, 118, 137, 152, 178, 202])
# INTENSITY_VALUES = np.array([5, 10, 17, 27, 41, 57, 74, 92, 124, 150, 176, 200])


def matching_field(variegated_array, ppd, field_size, field_intensity, field_pos=None):
    board_shape = variegated_array.shape
    check_visual_size = (1, 1)

    # Generate checkerboard
    checkerboard = stimupy.checkerboards.checkerboard(
        board_shape=board_shape, check_visual_size=check_visual_size, ppd=ppd
    )

    # Apply variegation
    checkerboard["img"] = stimupy.components.draw_regions(
        checkerboard["checker_mask"], intensities=variegated_array.flatten() / 255.0
    )

    # Overlay matching field
    field = stimupy.components.shapes.rectangle(
        visual_size=checkerboard["visual_size"],
        ppd=ppd,
        rectangle_size=field_size,
        intensity_rectangle=field_intensity,
    )
    combined = copy.deepcopy(checkerboard)
    combined["field_mask"] = field["rectangle_mask"]
    combined["img"] = np.where(combined["field_mask"], field["img"], checkerboard["img"])
    return combined


def load_variegated_array(filename="matchsurround.txt"):
    # Load variegated array from file
    variegated_array = np.fromtxt(Path(filename))

    # Permutate: flip surround, possibly multiple directions
    if random.choice((True, False)):
        variegated_array = np.fliplr(variegated_array)
    if random.choice((True, False)):
        variegated_array = np.flipud(variegated_array)

    return variegated_array


def gen_matching_fields_range(intensity_values, variegated_array, field_size, ppd, field_pos=None):
    # Base matching field
    field = matching_field(
        variegated_array=variegated_array,
        ppd=ppd,
        field_size=field_size,
        field_intensity=0,
        field_pos=field_pos,
    )

    # Generate matching fields for range of intensities of center patch
    matches = {}
    for intensity in intensity_values:
        this_field = copy.deepcopy(field)
        this_field["img"] = np.where(field["field_mask"], intensity, field["img"])
        matches[intensity] = this_field

    return matches


def export_matching_fields(filedir, matching_fields):
    # Check that output dir exists
    if not Path(filedir).exists():
        Path(filedir).mkdir(parents=True, exist_ok=True)

    # Export
    for intensity, matching_field in matching_fields.items():
        filename = f"match_{intensity:.3f}.bmp"
        array_to_image(matching_field["img"], Path(filedir) / filename, norm=True)


def direct_surround_from_image(fname):
    """
    read out surround indices for matches which were not saved upon generation
    """
    surround_pos = {
        "b2": (30, 30),
        "c2": (30, 60),
        "d2": (30, 90),
        "d3": (60, 90),
        "d4": (90, 90),
        "c4": (90, 60),
        "b4": (90, 30),
        "b3": (60, 30),
    }
    curr_stim = np.array(Image.open(fname).convert("L"))
    direct_surround_dict = {}
    for key, pos in surround_pos.iteritems():
        direct_surround_dict[key] = curr_stim[pos[0], pos[1]]
    return direct_surround_dict


if __name__ == "__main__":
    board_shape = (5, 5)
    ppd = 24
    field_size = 50 / ppd

    with Path("stimuli/match/trials_matchsurr.txt").open("w") as file:
        file.write("b2\tc2\td2\td3\td4\tc4\tb4\tb3\n")

        for trl_nr in np.arange(240):
            # Generate variegated array
            surround_values, direct_surround_dict = generate_variegated_array(
                INTENSITY_VALUES, board_shape
            )

            # Generate all possible matching intensities
            matching_fields = gen_matching_fields_range(
                intensity_values=np.linspace(0, 1, 256),
                variegated_array=surround_values,
                field_size=field_size,
                ppd=24,
                field_pos=None,
            )

            # Export matching fields
            filedir = f"stimuli/match/trl_{trl_nr:03d}"
            export_matching_fields(
                filedir=filedir,
                matching_fields=matching_fields,
            )

            # Record direct surround
            file.write(
                "%d\t%d\t%d\t%d\t%d\t%d\t%d\t%d\n"
                % (
                    direct_surround_dict["b2"],
                    direct_surround_dict["c2"],
                    direct_surround_dict["d2"],
                    direct_surround_dict["d3"],
                    direct_surround_dict["d4"],
                    direct_surround_dict["c4"],
                    direct_surround_dict["b4"],
                    direct_surround_dict["b3"],
                )
            )
