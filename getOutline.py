from PIL import Image, ImageFilter
import PIL.ImageOps

import cv2
import numpy as np

# TODO: modify script so it process image of arbitrary file name

# this loop ensures that image is inverted and filtered twice, so
# that we end up with colors in the right spot
for i in range(2):
    img = Image.open("Ball_rec0103.jpg")
    mask = img.convert("L")
    th = 150
    mask = mask.point(lambda i: i < th and 255)
    mask.save("mask_img.png")

    img = mask

    image = cv2.imread("mask_img.png")

    # convert to grayscale
    gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)

    # blur
    blur = cv2.GaussianBlur(gray, (0,0), sigmaX=33, sigmaY=33)

    # divide
    divide = cv2.divide(gray, blur, scale=255)

    # otsu threshold
    thresh = cv2.threshold(divide, 0, 255, cv2.THRESH_BINARY+cv2.THRESH_OTSU)[1]

    # apply morphology
    kernel = cv2.getStructuringElement(cv2.MORPH_RECT, (3,3))
    morph = cv2.morphologyEx(thresh, cv2.MORPH_CLOSE, kernel)

    cv2.imwrite("morph_img.jpg", morph)

    inverted_image = Image.open("morph_img.jpg")
    inverted_image = PIL.ImageOps.invert(inverted_image)
    inverted_image.save("Ball_rec0103.jpg")

# ******************************************************************
# the rest of this finds the "edges" and fills in black or white 
# where it can

# Reading the image saved from plot
image = cv2.imread('Ball_rec0103.jpg')

# Coversion to grayscale, inversion, edge detection
gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
gray = cv2.bitwise_not(gray)
edges = cv2.Canny(gray, 50, 200)

# Find the contours. The first two largest contours are for the outer contour
# So, taking the rest of the contours for inner contours
cnts = cv2.findContours(edges, cv2.RETR_LIST, cv2.CHAIN_APPROX_SIMPLE)
cnts = cnts[0] if len(cnts) == 2 else cnts[1]
cnts = sorted(cnts, key = cv2.contourArea, reverse = True)[2:]

# Filling the inner contours with black color
for c in cnts:
    cv2.drawContours(image, [c], -1, (0, 0, 0), -1)

# Displaying the result
cv2.imwrite("Contour.jpg", image)