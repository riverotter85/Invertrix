# Invertrix

A Python script that inverts image files vertically and/or horizontally using CUDA

## Description

Invertrix reads in a folder of images, where the user is then able to specify how each image will be inverted (if at all). The resulting output files are subsequently placed in a folder of the user's choosing. Depending on which options are selected, the files will display in the following format(s):

- ```vertical_<filename>```: The image is flipped vertically
- ```horizontal_<filename>```: The image is flipped horizontally
- ```both_<filename>```: The image is flipped both vertically and horizontally

The program uses Python's CUDA library in order to speed up image processing. Once the operation is complete, the final runtime is displayed before exiting. If the user specifies None as the option for an image, no new file is created.

## Prerequisites

Invertrix uses CUDA first and foremost, as well as a few other libraries including OpenCV, curses, and numpy. Additionally, you will need to have pypi installed on your system if it isn't already. Below is a list of commands for what you will need to install.

- Pypi: ```sudo apt-get install pypi```
- OpenCV: ```sudo pip install cv2```
- NumPy: ```sudo pip install numpy```
- Numba: ```sudo pip install numba```
- Curses: ```sudo pip install curses```

## How To Run

Once you have everything installed, you can execute the command ```./src/Invertrix.py``` or ```./src/Invertrix.py <args>``` from the Invertrix folder. Additionally, you can execute ```./run.sh```, which directly mimicks the results that are included in ```./data/artifacts```.

## Arguments

Invertrix has two command line arguments you can use to help customize where the software looks.

- ```-i <folder path>``` or ```--input <folder path>```: Changes the input directory where all the image files are read
- ```-o <folder path>``` or ```--output <folder path>```: Changes the output directory where all the new images are placed

## Controls

To help navigate Invertrix, an explanation for each keyset is provided below.

- ```ESC```: Exits the program
- ```UP```/```DOWN```: Navigates between the different images the program sees
- ```LEFT```/```RIGHT```: Navigates between invert operation(s) for the selected image
- ```ENTER```: Starts running invert operation(s) with the current configuration