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

img_files = []

def main():
    # Create list of image files to be read in and processed
    img_dir = os.fsencode("./data/")
    for file in os.listdir(img_dir):
        img_filename = os.fsdecode(file)
        if img_filename.endswith(".png"):
            img_files.append(img_filename)
    
    print("Hello!")
    
    for img_filename in img_files:
        image = cv2.imread(img_filename, cv2.IMREAD_COLOR)
        height = image.shape[0]
        width = image.shape[1]

        split_filename = os.path.split(img_filename)

        # Vertical invert
        new_image = np.zeros((height, width, 3))
        for y in range(0, height):
            for x in range(0, width):
                new_image[y, x] = image[255 - y, x]
        cv2.imwrite("./data/output/vertical/vertical_" + split_filename, new_image)

        # Horizontal invert
        new_image = np.zeros((height, width, 3))
        for y in range(0, height):
            for x in range(0, width):
                new_image[y, x] = image[y, 255 - x]
        cv2.imwrite("./data/output/horizontal/horizontal_" + split_filename, new_image)

        # Vertical and Horizontal invert
        new_image = np.zeros((height, width, 3))
        for y in range(0, height):
            for x in range(0, width):
                new_image[y, x] = image[255 - y, 255 - x]
        cv2.imwrite("./data/output/complete/complete_" + split_filename, new_image)


if __name__ == "__main__":
    main()