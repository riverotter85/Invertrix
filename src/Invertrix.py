#!/usr/bin/env python3

"""
Project Name: Invertrix
Description:

Filename: Invertrix.py
Author: Logan Davis
Date Created: 2/12/2024
Last Modified: 2/12/2024

"""

import os
import cv2
import numpy as np
from numba import jit
import curses
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
def completeInvert(img, height, width):
    new_image = np.zeros((height, width, 3))
    for y in range(0, height):
        for x in range(0, width):
            new_image[y, x] = img[height-y-1, width-x-1]
    
    return new_image

def detectInputFiles(dirPath):
    img_files = []

    img_dir = os.fsencode(dirPath)
    for file in os.listdir(img_dir):
        img_filename = os.fsdecode(file)
        if img_filename.endswith(".png"):
            img_files.append(img_filename)

    return img_files

def main(stdscr):
    img_files = detectInputFiles("./data/input")

    menuController = MenuController(stdscr, img_files)
    selectedOptions = menuController.prompt()
    
    menuController.setExecutionStatus("Starting inversion process on GPU...")
    menuController.showMenu()
    
    for img_filename in img_files:
        image = cv2.imread("./data/input/" + img_filename, cv2.IMREAD_COLOR)
        height = image.shape[0]
        width = image.shape[1]

        # Vertical Invert
        new_image = verticalInvert(image, height, width)
        cv2.imwrite("./data/output/vertical/vertical_" + img_filename, new_image)

        # Horizontal Invert
        new_image = horizontalInvert(image, height, width)
        cv2.imwrite("./data/output/horizontal/horizontal_" + img_filename, new_image)

        # Complete Invert
        new_image = completeInvert(image, height, width)
        cv2.imwrite("./data/output/complete/complete_" + img_filename, new_image)

    menuController.setExecutionStatus("Done! Press ANY KEY to exit.")
    menuController.showMenu()
    menuController.getKey()

if __name__ == "__main__":
    wrapper(main)