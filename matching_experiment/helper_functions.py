#!/usr/bin/env python
"""
Some functions used during experiments. 
For HRL on Python 2


Functions written over the years at the TU Vision group.

@author: MM, KZ, CW, TB and GA, collected by GA.
"""


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
