from PIL import Image

import os
import subprocess

# TODO: loops can be combined into one for better effeciency, look into implementing
# TODO: pass 'directory' as a command line argument

directory = os.fsencode("./")

# convert .jpg to .JPEG
for file in os.listdir(directory):
    file_name = os.fsdecode(file) # access .jpg file
    if file_name.endswith(".jpg"):
        base_name = os.path.splitext(file_name)[0] # remove file extension
        # convert from .jpg to .JPEG
        im = Image.open(file_name)
        im.save(base_name + ".JPEG")
        # clean up
        os.remove(file_name)

# convert .JPEG to DICOM file
for file in os.listdir(directory):
    file_name = os.fsdecode(file) # access .JPEG file
    if file_name.endswith(".JPEG"):
        base_name = os.path.splitext(file_name)[0] # remove file extension
        # convert from .JPEG to DICOM file
        subprocess.run(["img2dcm", file_name, base_name + ".dicom"])
        # clean up
        os.remove(file_name)