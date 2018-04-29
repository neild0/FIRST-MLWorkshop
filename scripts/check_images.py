import os

from PIL import Image

img_dir = "downloads"
for filename in os.listdir(img_dir):
    filepath = os.path.join(img_dir, filename)
    print('file folder >>>>>' + filepath)
    if filename == ".DS_Store":
        #print('DS folder -----'+filepath)
        os.remove(filepath)
    else:
        for imagename in os.listdir(filepath):

            imagepath = os.path.join(filepath, imagename)
            try:
                with Image.open(imagepath) as im:
                    n = 1
                    if im.format != "JPEG":
                        os.remove(imagepath)
            except:
                print(imagepath)
                os.remove(imagepath)
            if len(imagepath) > 220:
                os.remove(imagepath)
