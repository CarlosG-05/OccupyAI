import os
import glob

# Delete output image
if os.path.exists("output.jpg"):
    os.remove("output.jpg")

# Delete all section images
for img in glob.glob("section_*.jpg"):
    os.remove(img)