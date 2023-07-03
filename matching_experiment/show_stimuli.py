#!/usr/bin/env python
"""
Script to display a set of stimuli in the experimental monitor

GA.

"""

import glob
from socket import gethostname

import numpy as np
from hrl import HRL
from PIL import Image
from text_displays import text_to_arr

inlab_siemens = True if "vlab" in gethostname() else False
inlab_viewpixx = True if "viewpixx" in gethostname() else False


if inlab_siemens:
    # size of Siements monitor
    WIDTH = 1024
    HEIGHT = 768
    bg_blank = 0.1  # corresponding to 50 cd/m2 approx
    middlegap = 0

elif inlab_viewpixx:
    # size of VPixx monitor
    WIDTH = 1920
    HEIGHT = 1080
    bg_blank = 0.27  # corresponding to 50 cd/m2 approx
    middlegap = 150  # pixels

else:
    WIDTH = 1024
    HEIGHT = 768
    bg_blank = 0.27
    middlegap = 150  # pixels

# center of screen
whlf = WIDTH / 2.0
hhlf = HEIGHT / 2.0


def main(files):
    # We create the HRL object with parameters that depend on the setup we are using
    if inlab_siemens:
        # create HRL object
        hrl = HRL(
            graphics="datapixx",
            inputs="responsepixx",
            photometer=None,
            wdth=WIDTH,
            hght=HEIGHT,
            bg=bg_blank,
            scrn=1,
            lut="lut.csv",
            db=True,
            fs=True,
        )
    elif inlab_viewpixx:
        hrl = HRL(
            graphics="viewpixx",
            inputs="responsepixx",
            photometer=None,
            wdth=WIDTH,
            hght=HEIGHT,
            bg=bg_blank,
            scrn=1,
            lut="lut_viewpixx.csv",
            db=True,
            fs=True,
        )

    else:
        hrl = HRL(
            graphics="gpu",
            inputs="keyboard",
            photometer=None,
            wdth=WIDTH,
            hght=HEIGHT,
            bg=bg_blank,
            scrn=0,
            lut=None,
            db=True,
            fs=False,
        )

    # reading PNGs and converting to grayscale
    textures = []
    for fname in files:
        print("loading... %s " % fname)
        ## the image is loaded using PIL module and converted to a
        ## numpy array ranging from 0 to 1.
        image = Image.open(fname).convert("L")
        im = np.asarray(image) / 255.0

        # texture creation in buffer, input is numpy array [0-1]
        tex = hrl.graphics.newTexture(im)
        textures.append(tex)

    # generating text for filenames to be displayed
    texts = []
    for fname in files:
        im = text_to_arr(text=fname, intensity_background=0.27, intensity_text=0, fontsize=20)
        tex = hrl.graphics.newTexture(im)
        texts.append(tex)

    #######
    i = 0
    #######################################
    while True:
        tex = textures[i]
        tex.draw((whlf - tex.wdth / 2, hhlf - tex.hght / 2))

        tex = texts[i]
        tex.draw((100, 100))

        hrl.graphics.flip(clr=True)  # clr= True to clear buffer
        print("currently showing: %s" % files[i])

        (btn, t1) = hrl.inputs.readButton()
        # print btn

        if btn == "Space":
            break
        elif btn == "Right":
            i += 1
        elif btn == "Left":
            i -= 1

        if i < 0:
            i = len(textures) - 1
        if i == len(textures):
            i = 0

    # closing window
    hrl.close()


if __name__ == "__main__":
    files = glob.glob("stimuli/demo/*.png")
    main(files)


# EOF
