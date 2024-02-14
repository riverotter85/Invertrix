#!/usr/bin/env python3

"""
Project Name: Invertrix
Description:

Filename: Invertrix.py
Author: Logan Davis
Created: 2/12/2024
Last Modified: 2/14/2024

"""

import sys
import os
import cv2
import numpy as np
from numba import jit
from timeit import default_timer as timer
from curses import wrapper
from MenuController import MenuController

# CUDA GPU function that vertically inverts image
# Arguments:
# - img (Image): cv2 image that is being copied
# - height (int): Height of image
# - width (int): Width of image
# Returns: (Image)
@jit(target_backend='cuda')
def verticalInvert(img, height, width):
    new_image = np.zeros((height, width, 3))
    for y in range(0, height):
        for x in range(0, width):
            new_image[y, x] = img[height-y-1, x]
    
    return new_image

# CUDA GPU function that horizontally inverts image
# Arguments:
# - img (Image): cv2 image that is being copied
# - height (int): Height of image
# - width (int): Width of image
# Returns: (Image)
@jit(target_backend='cuda')
def horizontalInvert(img, height, width):
    new_image = np.zeros((height, width, 3))
    for y in range(0, height):
        for x in range(0, width):
            new_image[y, x] = img[y, width-x-1]
    
    return new_image

# CUDA GPU function that vertically and horizontally inverts image
# Arguments:
# - img (Image): cv2 image that is being copied
# - height (int): Height of image
# - width (int): Width of image
# Returns: (Image)
@jit(target_backend='cuda')
def bothInvert(img, height, width):
    new_image = np.zeros((height, width, 3))
    for y in range(0, height):
        for x in range(0, width):
            new_image[y, x] = img[height-y-1, width-x-1]
    
    return new_image

# Parses command line arguments, returning the appropriate input/output folder paths and execution status
# Arguments: None
# Returns: (String, String, String)
def parseCliArguments():
    inputDir = "./data/input"
    outputDir = "./data/output"
    status = ""

    i = 1
    while i+1 < len(sys.argv):
        if sys.argv[i] == "-i" or sys.argv[i] == "--input":
            inputDir = sys.argv[i+1]
            status += "Input folder set to '" + sys.argv[i+1] + "'. "
        elif sys.argv[i] == "-o" or sys.argv[i] == "--output":
            outputDir = sys.argv[i+1]
            status += "Output folder set to '" + sys.argv[i+1] + "'. "

        i += 2
    
    return inputDir, outputDir, status

# Gets list of valid image files within folder
# Arguments:
# - dirPath: path of folder we are checking
# Returns: (List)
def detectInputFiles(dirPath):
    img_files = []

    img_dir = os.fsencode(dirPath)
    for file in os.listdir(img_dir):
        img_filename = os.fsdecode(file)
        if img_filename.endswith(".png"):
            img_files.append(img_filename)

    return img_files

# Main function
# Arguments:
# - stdscr (stdscr): curses object passed from wrapper
# Returns: None
def main(stdscr):
    # Parse arguments and retrieve image files from input folder
    inputDir, outputDir, status = parseCliArguments()
    img_files = detectInputFiles(inputDir)

    # Show CLI menu and prompt user
    menuController = MenuController(stdscr, img_files)
    menuController.setExecutionStatus(status)
    selectedOptions = menuController.prompt()

    startTime = timer()
 
    # Show user that we're starting CUDA execution
    menuController.setExecutionStatus("Starting inversion process on GPU...")
    menuController.showMenu()
 
    # Work on each image file according to what the user specified
    for i in range(len(img_files)):
        # Get image info
        image = cv2.imread(inputDir + "/" + img_files[i], cv2.IMREAD_COLOR)
        height = image.shape[0]
        width = image.shape[1]

        # Vertical Invert
        if (selectedOptions[i] == 1):
            new_image = verticalInvert(image, height, width)
            cv2.imwrite(outputDir + "/vertical_" + img_files[i], new_image)
        # Horizontal Invert
        elif (selectedOptions[i] == 2):
            new_image = horizontalInvert(image, height, width)
            cv2.imwrite(outputDir + "/horizontal_" + img_files[i], new_image)
        # Complete Invert
        elif (selectedOptions[i] == 3):
            new_image = bothInvert(image, height, width)
            cv2.imwrite(outputDir + "/both_" + img_files[i], new_image)

    runTime = timer() - startTime

    # We're done! Show overall execution time
    menuController.setExecutionStatus("Completed in %.3fs. Press ANY KEY to exit." % runTime)
    menuController.showMenu()
    menuController.getKey()

if __name__ == "__main__":
    wrapper(main)