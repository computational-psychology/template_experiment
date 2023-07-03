#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
Some functions used during experiments. 
For HRL on Python 2


Functions written over the years at the TU Vision group.

@author: MM, KZ, CW, TB and GA, collected by GA.
"""

from PIL import Image, ImageFont, ImageDraw
import numpy as np


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
    im = Image.open("%s.%s" % (fname, in_format)).convert("L")
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


def draw_text(text, bg=0.27, text_color=0, fontsize=48):
    # function from Torsten
    """
    Create a numpy array containing the string text as an image.

    @author: TB
    """

    bg *= 255
    text_color *= 255
    font = ImageFont.truetype(
        "/usr/share/fonts/truetype/msttcorefonts/arial.ttf", fontsize, encoding="unic"
    )
    text_width, text_height = font.getsize(text)
    im = Image.new("L", (text_width, text_height), int(bg))
    draw = ImageDraw.Draw(im)
    draw.text((0, 0), text, fill=text_color, font=font)
    return np.array(im) / 255.0


# EOF
