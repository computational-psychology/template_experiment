import random
from pathlib import Path

import numpy as np
from PIL import Image
from stimupy.utils import array_to_image, resize_array
from variegate import generate_variegated_array

INTENSITY_VALUES = np.array([5, 10, 17, 27, 42, 57, 75, 96, 118, 137, 152, 178, 202])
# INTENSITY_VALUES = np.array([5, 10, 17, 27, 41, 57, 74, 92, 124, 150, 176, 200])


def replace_image_part(stimulus=None, replacement=None, position=None):
    """
    :Input:
    ----------
    stimulus    - numpy array of original stimulus
    increment   - numpy array of to be added increment
    position    - tuple of center coordinates within stimulus where increment should be placed
    :Output:
    ----------
    """

    inc_y, inc_x = replacement.shape
    pos_y, pos_x = position

    x1 = int(pos_x - inc_x / 2)
    x2 = int(pos_x + inc_x / 2)
    y1 = int(pos_y - inc_y / 2)
    y2 = int(pos_y + inc_y / 2)

    new_stimulus = stimulus.copy()

    for k, c in enumerate(range(x1, x2)):
        for l, r in enumerate(range(y1, y2)):
            new_stimulus[r, c] = replacement[l, k]
    return new_stimulus


def matching_field(variegated_array, resolution, field_size, field_intensity, field_pos=None):
    # Draw at full resolution
    surround = resize_array(variegated_array, factor=(resolution, resolution))

    # Generate matching field
    if not field_pos:
        field_pos = (surround.shape[0] // 2 - 1, surround.shape[1] // 2 - 1)
    field = np.ones((field_size, field_size)) * field_intensity

    # Draw
    match_stimulus = replace_image_part(surround, field, field_pos)

    return match_stimulus


def load_variegated_array(filename="matchsurround.txt"):
    # Load variegated array from file
    variegated_array = np.fromtxt(Path(filename))

    # Permutate: flip surround, possibly multiple directions
    if random.choice((True, False)):
        variegated_array = np.fliplr(variegated_array)
    if random.choice((True, False)):
        variegated_array = np.flipud(variegated_array)

    return variegated_array


def gen_matching_fields_range(
    intensity_values, variegated_array, field_size, resolution, field_pos=None
):
    # Generate matching fields for range of intensities of center patch
    matches = {}
    for intensity in intensity_values:
        matches[intensity] = matching_field(
            variegated_array=variegated_array,
            resolution=resolution,
            field_size=field_size,
            field_intensity=intensity,
            field_pos=field_pos,
        )

    # Add an extra array where the center target region has value=-1
    # so that we easily replace the values with the actual match value
    matches[-1] = matching_field(
        variegated_array=variegated_array,
        resolution=resolution,
        field_size=field_size,
        field_intensity=-1,
        field_pos=field_pos,
    )

    return matches


def export_matching_fields(filedir, matching_fields):
    # Check that output dir exists
    if not Path(filedir).exists():
        Path(filedir).mkdir(parents=True, exist_ok=True)

    # Export
    for intensity, matching_field in matching_fields.items():
        filename = f"match_{intensity:03d}.bmp"
        array_to_image(matching_field, Path(filedir) / filename, norm=False)


def read_surround_checks(fname):
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
    n_checks = 5
    field_size = 50
    resolution = 24

    with Path("stimuli/match/trials_matchsurr.txt").open("w") as file:
        file.write("b2\tc2\td2\td3\td4\tc4\tb4\tb3\n")

        for trl_nr in np.arange(240):
            # Generate variegated array
            surround_values, direct_surround_dict = generate_variegated_array(
                INTENSITY_VALUES, n_checks
            )

            # Generate all possible matching intensities
            matching_fields = gen_matching_fields_range(
                intensity_values=np.arange(255),
                variegated_array=surround_values,
                field_size=field_size,
                resolution=24,
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
