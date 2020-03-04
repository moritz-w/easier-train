# easier-train Tool

The purpose of this tool is to classify colors based on the users selection. An other tool for doing this already exits
called `easy train`.  But instead of asking the user to select a rectangular region `easier-train` uses an "algorithm" 
that automatically selects a colored area in an image based on the neighbour pixels and how similar
their color is. It is inspired by the "Magic Wand"-Tool that is offered by Photoshop or GIMP.
Additionally the user can select how the classified data should be saved (e.g. csv or sqlite) 

## Installation

**dependencies**:
```text
opencv-python (version: 4.2.0.32)
numpy (version: 1.18.1)
colour-science (version: 0.3.15)
PyQt5 (version: 5.13.1)
```

## Usage 

### Test Images

In the repository there are a few test images provided under `resoure/img/testimage*.png`. These are coordinates that 
will select the main color blob in the corresponding test image (e.g. for usage in the command line tool):

|image name|x,y coordinate|
|---|---|
`testimage1.png`| 71, 67
`testimage2.png`| 97, 97 

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


