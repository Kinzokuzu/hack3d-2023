import cv2
import os

dir_path = r"/Users/kinzo/Dev/hack3d-2023/fuck-this-shit-man/"

# convert .png files to .tiff
i = 0
for file_name in os.listdir(dir_path):
    image = cv2.imread(r"{}/{}".format(dir_path, file_name)) # open image
    cv2.imwrite(r"{}/{}.tiff".format(dir_path, i), image) # convert image
    i += 1
