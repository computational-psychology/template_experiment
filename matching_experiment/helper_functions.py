#!/usr/bin/env python
"""
Some functions used during experiments. 
For HRL on Python 2


Functions written over the years at the TU Vision group.

@author: MM, KZ, CW, TB and GA, collected by GA.
"""

import numpy as np
from PIL import Image


def image_to_array(fname, in_format="png"):
    # Function written by Marianne
    """
    Reads the specified image file (default: png), converts it to grayscale
    and into a numpy array

    Input:
    ------
    fname       - name of image file
    in_format   - extension (png default)

    Output:
    -------
    numpy array
    """
    im = Image.open(f"{fname}.{in_format}").convert("L")
    temp_matrix = [im.getpixel((y, x)) for x in range(im.size[1]) for y in range(im.size[0])]
    temp_matrix = np.array(temp_matrix).reshape(im.size[1], im.size[0])
    im_matrix = np.array(temp_matrix.shape, dtype=np.float64)
    im_matrix = temp_matrix / 255.0
    # print im_matrix
    return im_matrix


def read_design(fname):
    """
    Reads a design file in white-space separated format and stores the design matrix in
    a dictionary

    @author: MM.
    """
    design = open(fname)
    header = design.readline().strip("\n").split()
    print(header)
    data = design.readlines()

    new_data = {}

    for k in header:
        new_data[k] = []
    for l in data:
        curr_line = l.strip().split()
        for j, k in enumerate(header):
            new_data[k].append(curr_line[j])
    return new_data


def read_design_csv(fname):
    """
    Reads a design file in comma-separated format (CSV) and stores the design matrix in
    a dictionary, similarly to read_design()

    @author: GA.
    """

    design = open(fname)
    header = design.readline().strip("\n").split(",")
    # print header
    data = design.readlines()

    new_data = {}

    for k in header:
        new_data[k] = []
    for l in data:
        curr_line = l.strip().split(",")
        for j, k in enumerate(header):
            new_data[k].append(curr_line[j])
    return new_data


# EOF
