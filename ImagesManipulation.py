# Used for image manipulation
from PIL import Image
# Used for getting directory with the image collection
import os

# Will keep track of name & amount of degrees to counter rotate
i = 0

directory = "Hack-Gear"
for filename in os.listdir(directory):
    # Opens the images in order
    file_path = os.path.join(directory, filename)
    img = Image.open(file_path)

    # Counter rotates by i degrees 
    rot_img = img.rotate(-i)

    # Crops the edges for better results
    width, height = rot_img.size
    left = 100; top = 100; right = 3900; bottom = 3900
    crop_rot_img = rot_img.crop((left, top, right, bottom))

    # Names and saves images to current directory
    crop_rot_img.save("Ball_rec"+str(i)+".jpg")
    img.close()
    i += 1