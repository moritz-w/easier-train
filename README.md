# easier-train Tool

The purpose of this tool is to classify colors based on the users selection. An other tool for doing this already exits
called `easy train`.  But instead of asking the user to select a rectangular region `easier-train` uses an "algorithm" 
that automatically selects a colored area in an image based on the neighbour pixels and how similar
their color is. It is inspired by the "Magic Wand"-Tool that is offered by Photoshop or GIMP.
Additionally the user can select how the classified data should be saved (e.g. csv or sqlite) 

## Installation


## Usage 

### Test Images

In the repository there are a few test images provided under `resoure/img/testimage*.png`. These are coordinates that 
will select main the color blob in corresponding test image (e.g. for usage in the command line tool):

|image name|x,y coordinate|
|---|---|
`testimage1.png`| 71, 67
`testimage2.png`| 97, 97 

## How it works

This is just a sort section that describes how this tool works.

### Color detection
