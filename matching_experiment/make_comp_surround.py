import random
from pathlib import Path

import numpy as np
from PIL import Image
from stimupy.utils import array_to_image, resize_array

INTENSITY_VALUES = np.array([5, 10, 17, 27, 42, 57, 75, 96, 118, 137, 152, 178, 202])
# INTENSITY_VALUES = np.array([5, 10, 17, 27, 41, 57, 74, 92, 124, 150, 176, 200])


def position_constraint(random_array):
    """
    constraint 2: not 2 identical reflectances next to each other
    """
    n_rep = 0
    cnt = 1
    while cnt > 0:
        cnt = 0
        for j in np.arange(len(random_array)):
            ## check identity of adjacent reflectances for all but last and first
            if j < (len(random_array) - 1):
                if random_array[j] == random_array[j + 1]:
                    cnt = cnt + 1
            ## check identity of adjacent reflectances for last and first
            elif j == (len(random_array) - 1):
                if random_array[j] == random_array[0]:
                    cnt = cnt + 1

            # print 'idx %d, count %d' %(j, cnt)
        if cnt > 0:
            random.shuffle(random_array)
            n_rep = n_rep + 1
        else:
            break
    print(n_rep)
    return random_array


def position_constraint2(ext_surround, dir_surround):
    """
    constraint 2: not 2 identical reflectances next to each other
    """
    a = np.array((1, 2, 3, 5, 6, 7, 9, 10, 11, 13, 14, 15))
    b = np.array((0, 1, 2, 2, 3, 4, 4, 5, 6, 6, 7, 0))
    n_rep = 0
    cnt = 1
    while cnt > 0:
        cnt = 0
        cnt2 = 0
        for j in np.arange(len(ext_surround)):
            ## check identity of adjacent reflectances for all but last and first
            if j < (len(ext_surround) - 1):
                if ext_surround[j] == ext_surround[j + 1]:
                    cnt = cnt + 1
            ## check identity of adjacent reflectances for last and first
            elif j == (len(ext_surround) - 1):
                if ext_surround[j] == ext_surround[0]:
                    cnt = cnt + 1
            if j in a:
                if ext_surround[a[cnt2]] == dir_surround[b[cnt2]]:
                    cnt = cnt + 1

                cnt2 = cnt2 + 1

        # print cnt
        # print 'idx %d, count %d' %(j, cnt)
        if cnt > 0:
            random.shuffle(ext_surround)
            n_rep = n_rep + 1
        else:
            print("yes")
            break
    # print n_rep

    return ext_surround


def check_match_surrounds(surround_values):
    ext_surround = np.concatenate(
        (
            surround_values[0,],
            surround_values[1:4, 4],
            surround_values[4, range(4, -1, -1)],
            surround_values[range(3, 0, -1), 0],
        )
    )
    dir_surround = np.concatenate(
        (
            surround_values[1, 1:4],
            surround_values[2:4, 3],
            surround_values[3, range(2, 0, -1)],
            surround_values[range(2, 1, -1), 1],
        )
    )

    dir_surround = position_constraint(dir_surround)
    ext_surround = position_constraint2(ext_surround, dir_surround)

    surround_values[0,] = ext_surround[0:5]
    surround_values[1:4, 4] = ext_surround[5:8]
    surround_values[4, range(4, -1, -1)] = ext_surround[8:13]
    surround_values[range(3, 0, -1), 0] = ext_surround[13:16]

    surround_values[1, 1:4] = dir_surround[0:3]
    surround_values[2:4, 3] = dir_surround[3:5]
    surround_values[3, range(2, 0, -1)] = dir_surround[5:7]
    surround_values[range(2, 1, -1), 1] = dir_surround[7]

    return surround_values


def generate_variegated_array(values=np.array([]), n_checks=5):
    """
    return a side_length x side_length numpy array consisting of nr_int different values between min_in and max_int that are randomly arranged
    :input:
    --------
    values      - array of intensities from which to sample
    side_length - default=10

    :output:
    ---------
    numpy array
    """

    # Generate random array of indices
    index = np.random.randint(0, len(values), n_checks * n_checks)

    # Map indices to coordinates (e.g., d4)
    a = map(chr, range(97, 97 + n_checks))
    coordinates = {}
    cnt = 0
    for letters in a:
        for numbers in np.arange(1, 1 + n_checks):
            coordinates[letters + str(numbers)] = index[cnt]
            cnt = cnt + 1

    # Extract direct surround indices
    key_direct_surround = ["b2", "c2", "d2", "d3", "d4", "c4", "b4", "b3"]
    direct_surround = []
    for key in key_direct_surround:
        direct_surround.append(coordinates[key])

    # Check that no two identical gray values are next to each other
    direct_surround = position_constraint(np.array(direct_surround))
    for idx, key in enumerate(key_direct_surround):
        coordinates[key] = direct_surround[idx]

    # Lookup intensities from indices at coordinates
    surround_intensities = np.zeros((n_checks, n_checks))
    for col, letters in enumerate(map(chr, range(97, 97 + n_checks))):
        for row, numbers in enumerate(np.arange(1, 1 + n_checks)):
            surround_intensities[row, col] = values[coordinates[letters + str(numbers)]]

    # Sub-dict for immediate surround only
    direct_surround_dict = {key: coordinates[key] for key in key_direct_surround}

    return surround_intensities, direct_surround_dict


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


def image_to_array(fname, in_format="png"):
    """
    read specified image file (default: png), converts it to grayscale and into numpy array
    input:
    ------
    fname       - name of image file
    in_format   - extension (png default)
    output:
    -------
    numpy array
    """
    im = Image.open(f"{fname}.{in_format}").convert("L")
    im_matrix = [im.getpixel((y, x)) for x in range(im.size[1]) for y in range(im.size[0])]
    im_matrix = np.array(im_matrix).reshape(im.size[1], im.size[0])

    return im_matrix


def make_life_matches(
    field_size=50, resolution=24, intensity_values=np.arange(256), field_pos=None
):
    # Load variegated array from file
    variegated_array = np.fromtxt("matchsurround.txt")

    # Permutate: flip surround, possibly multiple directions
    if random.choice((True, False)):
        variegated_array = np.fliplr(variegated_array)
    if random.choice((True, False)):
        variegated_array = np.flipud(variegated_array)

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

    return matches, variegated_array


def make_single_trial_matches(
    trl_nr, n_checks=5, field_size=50, resolution=24, intensity_values=INTENSITY_VALUES
):
    """
    generate all possible matches for LUT of [0,255]
    returns:
    - reflectance index [1,12] for the checks adjacent to match
    - 256 bmps with match intensities on constant surround
    """
    # Generate variegated array
    surround_values, direct_surround_dict = generate_variegated_array2(
        intensity_values=intensity_values, n_checks=n_checks
    )

    # Generate files for all possible matching fields
    filedir = f"stimuli/match/trl_{trl_nr:03d}"
    export_matching_fields(
        filedir=filedir,
        variegated_array=surround_values,
        field_size=field_size,
        resolution=resolution,
        intensity_values=np.arange(256),
    )

    return direct_surround_dict


def export_matching_fields(
    filedir,
    variegated_array,
    field_size,
    resolution,
    intensity_values=np.arange(256),
    field_pos=None,
):
    # Check that output dir exists
    if not Path(filedir).exists():
        Path(filedir).mkdir(parents=True, exist_ok=True)

    # Generate matching fields for range of intensities of center patch
    for intensity in intensity_values:
        match_stimulus = matching_field(
            variegated_array=variegated_array,
            resolution=resolution,
            field_size=field_size,
            field_intensity=intensity,
            field_pos=field_pos,
        )

        filename = f"match_{intensity:03d}.bmp"
        array_to_image(match_stimulus, Path(filedir) / filename, norm=False)


def generate_variegated_array2(intensity_values=INTENSITY_VALUES, n_checks=5):
    """
    Also checks that the mean of the overall array,
    as well as the mean of the immediate surround,
    is (approx.) equal to the mean of the given intensity values
    """

    valid = False
    while not valid:
        surround_values, direct_surround = generate_variegated_array(intensity_values, n_checks)
        surround_values = check_match_surrounds(surround_values)

        # the center check should not add to the mean, therefore it is replaced by the mean
        adj_surr = np.array(
            (
                surround_values[1, 1],
                surround_values[1, 2],
                surround_values[1, 3],
                surround_values[2, 1],
                surround_values[2, 3],
                surround_values[3, 1],
                surround_values[3, 2],
                surround_values[3, 3],
            )
        )
        surround_values[2, 2] = round(np.mean(intensity_values))
        match_mean = round(np.mean(surround_values))
        surround_mean = round(np.mean(adj_surr))
        if match_mean == round(np.mean(intensity_values)) and surround_mean == round(
            np.mean(intensity_values)
        ):
            valid = True

    return surround_values


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
    curr_stim = image_to_array(fname, "bmp")
    direct_surround_dict = {}
    for key, pos in surround_pos.iteritems():
        direct_surround_dict[key] = curr_stim[pos[0], pos[1]]
    return direct_surround_dict


if __name__ == "__main__":
    with Path("stimuli/match/trials_matchsurr.txt").open("w") as file:
        file.write("b2\tc2\td2\td3\td4\tc4\tb4\tb3\n")

        for trl_nr in np.arange(240):
            direct_surround_dict = make_single_trial_matches(trl_nr)
            # match_surr = read_surround_checks('stimuli/match/%03d_match_000' %trl_nr)
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
