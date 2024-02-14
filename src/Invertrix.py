#!/usr/bin/env python3

"""
Project Name: Invertrix
Description:

Filename: Invertrix.py
Author: Logan Davis
Date Created: 2/12/2024
Last Modified: 2/12/2024

"""

import sys
import os
import cv2
import numpy as np
from numba import jit
from curses import wrapper
from MenuController import MenuController

@jit(target_backend='cuda')
def verticalInvert(img, height, width):
    new_image = np.zeros((height, width, 3))
    for y in range(0, height):
        for x in range(0, width):
            new_image[y, x] = img[height-y-1, x]
    
    return new_image

@jit(target_backend='cuda')
def horizontalInvert(img, height, width):
    new_image = np.zeros((height, width, 3))
    for y in range(0, height):
        for x in range(0, width):
            new_image[y, x] = img[y, width-x-1]
    
    return new_image

@jit(target_backend='cuda')
def bothInvert(img, height, width):
    new_image = np.zeros((height, width, 3))
    for y in range(0, height):
        for x in range(0, width):
            new_image[y, x] = img[height-y-1, width-x-1]
    
    return new_image

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

def detectInputFiles(dirPath):
    img_files = []

    img_dir = os.fsencode(dirPath)
    for file in os.listdir(img_dir):
        img_filename = os.fsdecode(file)
        if img_filename.endswith(".png"):
            img_files.append(img_filename)

    return img_files

def main(stdscr):
    inputDir, outputDir, status = parseCliArguments()
    img_files = detectInputFiles(inputDir)

    menuController = MenuController(stdscr, img_files)
    menuController.setExecutionStatus(status)
    selectedOptions = menuController.prompt()
    
    menuController.setExecutionStatus("Starting inversion process on GPU...")
    menuController.showMenu()
    
    for i in range(len(img_files)):
        image = cv2.imread(inputDir + "/" + img_files[i], cv2.IMREAD_COLOR)
        height = image.shape[0]
        width = image.shape[1]

        if (selectedOptions[i] == 1):
            # Vertical Invert
            new_image = verticalInvert(image, height, width)
            cv2.imwrite(outputDir + "/vertical_" + img_files[i], new_image)
        elif (selectedOptions[i] == 2):
            # Horizontal Invert
            new_image = horizontalInvert(image, height, width)
            cv2.imwrite(outputDir + "/horizontal_" + img_files[i], new_image)
        elif (selectedOptions[i] == 3):
            # Complete Invert
            new_image = bothInvert(image, height, width)
            cv2.imwrite(outputDir + "/both_" + img_files[i], new_image)

    menuController.setExecutionStatus("Done! Press ANY KEY to exit.")
    menuController.showMenu()
    menuController.getKey()

if __name__ == "__main__":
    wrapper(main)