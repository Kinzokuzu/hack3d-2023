# Used for image manipulation
from PIL import Image
import PIL.ImageOps
import cv2
# Used for getting directory with the image collection
import os

# SET THIS TO THE PATH OF YOUR PYTHON SCRIPT
os.chdir(r"C:\Users\name\etc")

# *************************************************************************************
# Creates a new directory and stores cropped + rotated images from original directory

# Will keep track of image number & amount of degrees to counter rotate
x = 0

# SET THIS TO THE PATH OF YOUR ORIGINAL IMAGES 
# (for ease of use put the dir in the same location as the python script)
dir = "Original"

# A new directory to store the rotated + cropped images
new_dir = "Cropped&Rotated"
os.mkdir(new_dir)

# Will iterate through the original directory rotating, cropping, and saving them to new directory
for image in os.listdir(dir):

    # Creates path to current images and opens it with PIL
    path = os.path.join(dir, image)
    img = Image.open(path)

    # Counter rotates by i degrees 
    rot_img = img.rotate(-x)

    # Crops the edges
    width, height = rot_img.size
    left = 100; top = 100; right = 3900; bottom = 3900
    crop_rot_img = rot_img.crop((left, top, right, bottom))

    # Names and saves images to new directory
    crop_rot_img.save(f"{new_dir}/Ball_rec"+str(x)+".jpg")
    img.close()
    x += 1

# *************************************************************************************
# Adds a filter to those new images to remove grain and fixs all colour to either 0 or 255

# Will keep track of image number
x = 0

# Switches to the newly created directory
dir = new_dir

# A new directory to store all masks and inverted images
new_dir = "Masks&InvertedImages"
os.mkdir(new_dir)

# A final directory to store all the final results
final_dir = "Result"
os.mkdir(final_dir)

# Creates new filtered image from the new images
for image in os.listdir(dir):

    # Ensures that every image is inverted and filtered twice, 
    # so that we end up with colors in the right spot
    for i in range(2):

        # first loop: opens image from rotated + cropped images
        # second loop: opens newly created inverted imgage
        if i == 0:
            path = os.path.join(dir, image)
        else:
            path = f"{new_dir}/inverted_img"+str(x)+".jpg"
        img = Image.open(path)

        # Creates a mask of image that [NO FKN CLUE HONESTLY]
        mask = img.convert("L")
        th = 150
        mask = mask.point(lambda i: i < th and 255)
        mask.save(f"{new_dir}/mask_img"+str(x)+".png")

        img = mask

        image = cv2.imread(f"{new_dir}/mask_img"+str(x)+".png")

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

        cv2.imwrite(f"{new_dir}/morph_img"+str(x)+".jpg", morph)

        inverted_image = Image.open(f"{new_dir}/morph_img"+str(x)+".jpg")
        inverted_image = PIL.ImageOps.invert(inverted_image)
        inverted_image.save(f"{new_dir}/inverted_img"+str(x)+".jpg")
        img.close()

    # ******************************************************************
    # the rest of this finds the "edges" and fills in black or white

    # Reading the image saved from plot
    image = cv2.imread(f"{new_dir}/inverted_img"+str(x)+".jpg")

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
    cv2.imwrite(f"{final_dir}/Ball_rec"+str(x)+".jpg", image)

    x += 1