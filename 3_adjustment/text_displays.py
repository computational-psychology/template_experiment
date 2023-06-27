import numpy as np
from hrl.graphics import graphics
from PIL import Image, ImageDraw, ImageFont


def text_to_arr(text, intensity_text=0.0, intensity_background=0.2, fontsize=36):
    """Draw given text into a (numpy) image-array

    Parameters
    ----------
    text : str
        Text to draw
    intensity_text : float, optional
        intensity of the text in range (0.0; 1.0), by default 0.0
    intensity_background : float, optional
        intensity of the background in range (0.0; 1.0), by default 0.2
    fontsize : int, optional
        font size, by default 36

    Returns
    -------
    np.ndarray
        image-array with text drawn into it,
        intensities in range (0.0; 1.0)
    """

    # @author: Torsten Betz; Joris Vincent

    # Try to load the font
    try:
        # Not all machines will have Arial installed...
        font = ImageFont.truetype(
            "/usr/share/fonts/truetype/msttcorefonts/arial.ttf",
            fontsize,
            encoding="unic",
        )
    except IOError:
        # On Ubuntu, should have the Ubuntu Mono fonts
        font = ImageFont.truetype(
            "/usr/share/fonts/truetype/Ubuntu/UbuntuMono-R.ttf",
            fontsize,
            encoding="unic",
        )

    # Determine dimensions of total text
    text_width, text_height = font.getsize(text)

    # Instantiate grayscale image of correct dimensions and background
    img = Image.new("L", (text_width, text_height), int(intensity_background * 255))

    # Draw text into this image
    draw = ImageDraw.Draw(img)
    draw.text((0, 0), text, fill=int(intensity_text * 255), font=font)

    # Downscale image-array to be in range (0.0; 1.0)
    return np.array(img) / 255.0


def display_text(
    ihrl,
    text,
    fontsize=36,
    intensity_text=0.0,
    intensity_background=0.2,
    window_shape=(1024, 768),
):
    """Display a screen with given text, waiting for participant to press button

    Text will be center horizontally.

    Parameters
    ----------
    ihrl : hrl
        HRL-interface object to use for display and input
    text : str, list[str]
        text to display, can be multiple lines
    fontsize : int, optional
        font size, by default 36
    intensity_text : float, optional
        intensity of the text in range (0.0; 1.0), by default 0.0
    intensity_background : float, optional
        intensity of the background in range (0.0; 1.0), by default 0.2
    window_shape : (int, int)
        shape (in pixels) of the HRL window, by default (1024, 768)
    """

    # Draw each line of text, one at a time
    for line_nr, line in enumerate(text):
        # Generate image-array, OpenGL texture
        if line == "":
            line = " "
        text_arr = text_to_arr(
            text=line,
            intensity_text=intensity_text,
            intensity_background=intensity_background,
            fontsize=fontsize,
        )
        textline = ihrl.graphics.newTexture(text_arr)

        # Determine position
        text_pos = (
            (window_shape[1] - textline.wdth) // 2,
            ((window_shape[0] // 2) - ((len(text) // 2) - line_nr) * (textline.hght + 10)),
        )

        # Draw line
        textline.draw(pos=text_pos)

    # Display
    ihrl.graphics.flip(clr=True)

    # Cleanup: delete texture
    graphics.deleteTextureDL(textline._dlid)

    return
