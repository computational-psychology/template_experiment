#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Plot raw eye tracking data using pygaze

https://osdoc.cogsci.nl/3.2/manual/eyetracking/pygaze/


@author: G. Aguilar July 2023

"""
import os
import numpy
import pandas as pd

from pygazeanalyser.edfreader import read_edf
from pygazeanalyser.gazeplotter import draw_fixations, draw_heatmap, draw_scanpath, draw_raw


# DATA FILES
SEP = '\t' # value separator
EDFSTART = "TRIALID" # EDF file trial start message
EDFSTOP = "TRIAL_RESULT" # EDF file trial end message
TRIALORDER = [EDFSTART, 'image_onset','blank_screen', EDFSTOP]
INVALCODE = 0.0 # value coding invalid data

# EXPERIMENT SPECS
DISPSIZE = (1920,1080) # (px,px)
SCREENSIZE = (53.3, 30) # (cm,cm)
SCREENDIST = 76.0 # cm
PXPERCM = numpy.mean([DISPSIZE[0]/SCREENSIZE[0],DISPSIZE[1]/SCREENSIZE[1]]) # px/cm


observer = 'demo'
block = 1


# for one block first

fp = os.path.join('../results/', observer, 'EDF', '%s0%d.asc' % (observer, block))

# read gaze data
edfdata = read_edf(fp, EDFSTART, stop=EDFSTOP, missing=INVALCODE, debug=True)

# read responses
data = pd.read_csv('../results/%s/block_%d.csv' % (observer,block))

assert(len(data)==len(edfdata))


pplotdir = '../plots/'

# loop through trials
for trialnr in range(len(data)):
           
    # load image name, saccades, and fixations
    imagefile = '../stimuli/demo/block_%d_%d.png' % (block, trialnr)
    
    saccades = edfdata[trialnr]['events']['Esac'] # [starttime, endtime, duration, startx, starty, endx, endy]
    fixations = edfdata[trialnr]['events']['Efix'] # [starttime, endtime, duration, endx, endy]
          
    # paths
    rawplotfile = os.path.join(pplotdir, "raw_data_%s_%d_%d" % (observer, block, trialnr))
    scatterfile = os.path.join(pplotdir, "fixations_%s_%d_%d" % (observer, block, trialnr))
    scanpathfile =  os.path.join(pplotdir, "scanpath_%s_%d_%d" % (observer, block, trialnr))
    heatmapfile = os.path.join(pplotdir, "heatmap_%s_%d_%d" % (observer, block, trialnr))
          
    # raw data points
    draw_raw(edfdata[trialnr]['x'], edfdata[trialnr]['y'], DISPSIZE, imagefile=imagefile, savefilename=rawplotfile)
  
    # fixations
    draw_fixations(fixations, DISPSIZE, imagefile=imagefile, durationsize=True, durationcolour=False, alpha=0.5, savefilename=scatterfile)
          
    # scanpath
    draw_scanpath(fixations, saccades, DISPSIZE, imagefile=imagefile, alpha=0.5, savefilename=scanpathfile)
  
    # heatmap        
    draw_heatmap(fixations, DISPSIZE, imagefile=imagefile, durationweight=True, alpha=0.5, savefilename=heatmapfile)

