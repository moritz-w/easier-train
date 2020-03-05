# easier-train Tool

The purpose of this tool is to classify colors based on the users selection. An other tool for doing this already exits
called `easy train`.  But instead of asking the user to select a rectangular region `easier-train` uses an "algorithm" 
that automatically selects a colored area in an image based on the neighbour pixels and how similar
their color is. It is inspired by the "Magic Wand"-Tool that is offered by Photoshop or GIMP.

## Installation

Make sure you have the dependencies installed with `pip`. Then simply execute the `easier-train` python script. 

**Dependencies**:
```text
Python 3.7
------------
opencv-python (version: 4.2.0.32)
numpy (version: 1.18.1)
colour-science (version: 0.3.15)
PyQt5 (version: 5.13.1)
```

## Usage 

The first argument to the command line is the path to load the images from. If no path is given, the directory from 
where the script was started is used:

```shell script
python3 easier-train.py /home/user/Pictures 
```

#### User Interface

![](https://i.imgur.com/GpcD44z.png)

As shown in the screenshot above the UI is divided into 3 parts. On the left hand side you can choose a PNG image that
will be shown in the center of the UI. The toolbar at the bottom can be used for classification.

To actually select a color click on a pixel in the image. The red/pink(ish) outline shows which pixels where selected.
You can then classify the selected pixels with the classify button in the toolbar or chose more pixels. The selection
of pixels is not saved when switching between images. Clicking the reset button will restore the original image.  

![](https://i.imgur.com/HGom026.png)

## How it works

This is just a sort section that describes how this tool works.

### Color detection

From the starting point given by the user a simple flood fill algorithm will check if nearby pixels have
a similar color by calculating the color difference with the so called `delta E` formula. ([Wikipedia article](https://en.wikipedia.org/wiki/Color_difference#CIELAB_%CE%94E*)) 

### Classification

For classification each color channel of the class gets assigned to a lookup table. To look up if 
a color is part of a class a bitwise `AND` operation  is done for the respective RGB value in the corresponding
lookup table. ([Realtime Machine Vision Perception and
Prediction Paper](http://www.cs.cmu.edu/~jbruce/cmvision/papers/JBThesis00.pdf))


