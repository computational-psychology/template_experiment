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


def make_random_array(values=np.array([]), n_checks=5):
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

    index = np.random.randint(0, len(values), n_checks * n_checks)

    a = map(chr, range(97, 97 + n_checks))

    positions = {}
    cnt = 0
    ## create dictionary with coordinate (e.g. d4):index pairs
    for letters in a:
        for numbers in np.arange(1, 1 + n_checks):
            positions[letters + str(numbers)] = index[cnt]
            cnt = cnt + 1

    surround_checks = ["b2", "c2", "d2", "d3", "d4", "c4", "b4", "b3"]

    ## read gray values at surround positions from position dictionary
    surround_int = []
    for surr_name in surround_checks:
        surround_int.append(positions[surr_name])

    ## check that no two identical gray values are next to each other
    surround_control = position_constraint(np.array(surround_int))

    surround_control_dict = {}
    for idx, surr_name in enumerate(surround_checks):
        positions[surr_name] = surround_control[idx]
        ## sub dictionary for immediate surround only
        surround_control_dict[surr_name] = surround_control[idx]

    out = np.zeros((n_checks, n_checks))

    for col, letters in enumerate(a):
        for row, numbers in enumerate(np.arange(1, 1 + n_checks)):
            out[row, col] = values[positions[letters + str(numbers)]]
    return out, surround_control_dict


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


def make_life_matches(center_size=50, resolution=24, intensity_values=np.arange(256)):
    # Load variegated array from file
    surround_values = np.fromtxt("matchsurround.txt")

    # Permutate: flip surround, possibly multiple directions
    if random.choice((True, False)):
        surround_values = np.fliplr(surround_values)
    if random.choice((True, False)):
        surround_values = np.flipud(surround_values)

    # Draw at full resolution
    surround = resize_array(surround_values, (resolution, resolution))

    # Generate center patch
    if not center_pos:
        center_pos = (surround.shape[0] // 2 - 1, surround.shape[1] // 2 - 1)
    center = np.ones((center_size, center_size))

    # Generate matching fields for range of intensities of center patch
    matches = {}
    for intensity in intensity_values:
        matches[intensity] = replace_image_part(surround, center * intensity, center_pos)

    # Add an extra array where the center target region has value=-1
    # so that we easily replace the values with the actual match value
    matches[-1] = replace_image_part(surround, center * -1, center_pos)

    return matches, surround_values


def make_single_trial_matches(
    trl_nr, n_checks=5, center_size=50, resolution=24, intensity_values=INTENSITY_VALUES
):
    """
    generate all possible matches for LUT of [0,255]
    returns:
    - reflectance index [1,12] for the checks adjacent to match
    - 256 bmps with match intensities on constant surround
    """
    # Generate variegated array
    surround_values, direct_surround = make_random_array(intensity_values, n_checks)

    # Draw at full resolution
    surround = resize_array(surround_values, factor=(resolution, resolution))

    # Generate files for all possible matching fields
    filedir = f"stimuli/match/trl_{trl_nr:03d}"
    export_matching_fields(
        surround=surround,
        filedir=filedir,
        center_size=center_size,
        intensity_values=np.arange(256),
    )

    return direct_surround


def export_matching_fields(
    surround, filedir, center_size, intensity_values=np.arange(256), center_pos=None
):
    # Generate center patch
    if not center_pos:
        center_pos = (surround.shape[0] // 2 - 1, surround.shape[1] // 2 - 1)
    center = np.ones((center_size, center_size))

    # Check that output dir exists
    if not Path(filedir).exists():
        Path(filedir).mkdir(parents=True, exist_ok=True)

    # Generate matching fields for range of intensities of center patch
    for intensity in intensity_values:
        match_stimulus = replace_image_part(surround, center * intensity, center_pos)

        filename = f"match_{intensity:03d}.bmp"
        array_to_image(match_stimulus, Path(filedir) / filename, norm=False)


def make_life_single_trial_matches(
    n_checks=5, center_size=50, resolution=24, intensity_values=INTENSITY_VALUES
):
    """
    generate all possible matches for LUT of [0,255]
    returns:
    - reflectance index [1,12] for the checks adjacent to match
    - numpy array
    """

    ind = 0
    while ind < 1.0:
        surround_values, direct_surround = make_random_array(intensity_values, n_checks)
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
            ind = 1
        if ind == 1:
            break

    return surround_values
    # surround_values = check_match_surrounds(surround_values)

    ## draw to scale
    surround = resize_array(surround_values, (resolution, resolution))

    pos = np.round(surround.shape[0] / 2) - 1

    matches = {}

    ## modify match intensity on constant surround
    for center_int in np.arange(256):
        center = np.ones((center_size, center_size)) * center_int
        matches[center_int] = replace_image_part(surround, center, (pos, pos))
    return matches, direct_surround, surround_values


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
    direct_surround = {}
    for idx, pos in surround_pos.iteritems():
        direct_surround[idx] = curr_stim[pos[0], pos[1]]
    return direct_surround


if __name__ == "__main__":
    with Path("stimuli/match/trials_matchsurr.txt").open("w") as file:
        file.write("b2\tc2\td2\td3\td4\tc4\tb4\tb3\n")

        for trl_nr in np.arange(240):
            match_surr = make_single_trial_matches(trl_nr)
            # match_surr = read_surround_checks('stimuli/match/%03d_match_000' %trl_nr)
            file.write(
                "%d\t%d\t%d\t%d\t%d\t%d\t%d\t%d\n"
                % (
                    match_surr["b2"],
                    match_surr["c2"],
                    match_surr["d2"],
                    match_surr["d3"],
                    match_surr["d4"],
                    match_surr["c4"],
                    match_surr["b4"],
                    match_surr["b3"],
                )
            )
