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

img_files = []

def main():
    # Create list of image files to be read in and processed
    img_dir = os.fsencode("./data/")
    for file in os.listdir(img_dir):
        img_filename = os.fsdecode(file)
        if img_filename.endswith(".png"):
            img_files.append(img_filename)
    
    for img_file in img_files:
        img = cv2.imread(img_file, cv2.IMREAD_COLOR)

        rows = img.shape[0]
        cols = img.shape[1]
        for row in range(0, rows):
            for col in range(0, cols):
                img[row, col] = 255 # TODO: Change this to swap start and end pixels

if __name__ == "__main__":
    main()