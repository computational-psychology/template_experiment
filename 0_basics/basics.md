# Basic experiment code using HRL

This folder demonstrates
-- and can serve as a template for --
 the basics of running an experiment.

In general, coding up an experiment requires:
- displaying some stimulus (e.g., an image)
- collecting some responses (e.g., button presses) from a participant

There are many tools and libraries available to take care of some of the technicalities,
such as interacting with hardware (monitor, keyboard/buttonbox).
Here, we use our [HRL](https://github.com/computational-psychology/hrl) package
to display stimuli and capture responses.

In addition to these core tasks, an experiment also involves
- defining, generating, or loading what stimulus/stimuli to use
- processing the captured participant responses (e.g., saving, presenting a new stimulus,...)
- coordinating these various steps

For that, we as the experiment will have to write our own code
-- in this demo/template that is `experiment.py`

```mermaid
graph LR;
    setup --> define --> display --> capture --> process --> cleanup

    subgraph experiment.py
        setup
        define[define stimulus]

        process[process - do something - with response]
        cleanup
    end

    subgraph HRL
        display[display stimulus]
        capture[capture participant response]
    end
```

## - Installation

Install [HRL](https://github.com/computational-psychology/hrl):
```bash
pip install https://github.com/computational-psychology/hrl/archive/master.zip
```

This will also install the required dependencies:
- [PyOpenGL](https://pyopengl.sourceforge.net/) (`pyopengl`)
- [PyGame](https://www.pygame.org/) (`pygame`)
- [NumPy](https://numpy.org/) (`numpy`)

## 0. Setup
To use HRL's functionality, we have to create a specific `hrl`-object.
We can then use methods from this object, to control the display
and get responses.
This takes some arguments, such as:
- `wdth`,`hght`: the resolution (width and height) of the window to draw
- `fs`: whether to fullscreen the window
- `scrn`: index of which screen (monitor) to use in a multimonitor setup
- `graphics`: which graphics device to use -- "gpu", or "datapixx" in the lab
- `inputs`: which input device to use -- "keyboard", or "responsepixx" in the lab

```python
from hrl import HRL

# Define window parameters
SHAPE = (1024, 1024)  # Desired shape of the drawing window

# Create HRL interface object
ihrl = HRL(
    graphics="gpu",  # Use the default GPU as graphics device driver
    # graphics='datapixx',    # In the lab, we use the datapixx device driver
    inputs="keyboard",  # Use the keyboard as input device driver
    # inputs="responsepixx",  # In the lab, we use the responsepixx input device
    hght=SHAPE[0],
    wdth=SHAPE[1],
    scrn=0,  # Which screen (monitor) to use
    fs=False,  # Fullscreen?
)
```

## 1. Define stimulus
In order to display a stimulus,
we first have to define/load/create a stimulus.
There are many ways to do so,
e.g., load an image from a file.
Here, create an image-matrix (np.ndarray) with 256x256 random values
```python
import numpy as np

rng = np.random.default_rng()
stim_image = rng.standard_normal(size=(256, 256))
```

## 2. Display stimulus
To display on the screen HRL uses frame buffers.
We can draw OpenGL primitives and textures on a frame buffer
and then when we want to display that on the screen,
we "flip" the buffer.

First, we convert our stimulus to an OpenGL texture,
then we place that on the frame buffer,
and then we flip the buffer

```python
# Convert the stimulus image(matrix) to an OpenGL texture
stim_texture = ihrl.graphics.newTexture(stim_image)

# Determine position: we want the stimulus in the center of the frame
CENTER = (SHAPE[0] // 2, SHAPE[1] // 2)  # Center of the drawing window
pos = (CENTER[1] - (stim_texture.wdth // 2), CENTER[0] - (stim_texture.hght // 2))

# Create a display: draw texture on the frame buffer
stim_texture.draw(pos=pos, sz=(stim_texture.hght, stim_texture.wdth))

# Display: flip the frame buffer
ihrl.graphics.flip(clr=True)  # also `clear` the frame buffer
```

The stimulus display will then stay on the screen
until either another `.flip()` is called,
or the hrl-object is `.close()`'d

## 3. Capture participant response
After displaying some stimulus, we often want some response from the participant.
This generally requires two steps:
- capturing the response via some input hardware (e.g., keyboard, button box)
- "processing" the response, i.e., deciding what to do with it
  (determine next stimulus, record to disk, etc.)

HRL also provides functionality to interact with input hardware.
The high-level interface is `<hrl_object>.inputs.readButton()`,
which waits for a (single) button press.

By default, `readButton` waits until one of the following buttons is pressed:
"Up", "Down", "Right", "Left", "Space", "Escape"
```python
ihrl.inputs.readButton()

print("Participant pressed a button")
```

`readButton`can also be asked to respond to only some buttons
and ignore all others:
```python
ihrl.inputs.readButton(btns=("Right", "Space", "Left", "Escape"))

print("Participant pressed a button")
```

`readButton` also returns a tuple
of a string-descriptor of the button pressed,
and the response delay (i.e., time until button was pressed).
```python
button, t1 = ihrl.inputs.readButton()

print(f"Participant pressed {button} after {t1}s")
```

## 4. Process response
Having captured a response, we need to process it.
This can include all kinds of steps, for instance
deciding if the response is "correct" or not (in tasks where this is possible);
storing the response (and additional information) as results data;
deciding what the next trial & stimulus will be.

```python
# Assign responses to correct/incorreect
response_correct = {"Right": True, "Left": False, "Escape": False}

if response_correct[button]:
    print(f"Participant pressed {button}, which is correct")
else:
    print(f"Participant pressed {button}, which is incorrect")
```

How exactly the response is mapped to some action
depends heavily on the experiment and task.
For example, in a Method of Forced Choice experiment,
the response is converted to correct/incorrect,
recorded as a result, and a new trial is presented.

In a Method of Adjustment task
the response leads to increasing/decreasing some stimulus level.
In these experiments, a button press will lead to a new _stimulus display_,
but not immediately to recording a new result.
Only when some other button is pressed to _accept_ a match,
then the result is recorded and a new trial is started.


## Cleanup
After the whole experiment is done 
(or if the participant/experimenter wants to terminate earlier),
some cleanup is required:
the connection to display and input hardware should be closed.
This can be done using the `.close()` method of the HRL-object.
```python
ihrl.close()
```