from PIL import Image
from pytesseract import image_to_string
from googletrans import Translator
import argparse
import cv2
import os
import docx

ap = argparse.ArgumentParser()
ap.add_argument("--image", required = True,
                help = 'Name of the image file')
ap.add_argument("--preprocess", type=str, default = "thresh",
                help = 'Preprocessing method (thresholding by default)')
ap.add_argument("--extension", type=str, default = "png",
                help = 'Extension of image file (png by default)')
ap.add_argument("--langcode", type=str, required = True,
                help = 'Language code of language to be translated to')
args = vars(ap.parse_args())

image = cv2.imread(args["image"])
gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)

if args["preprocess"] == "thresh":
    gray = cv2.threshold(gray, 0, 255, cv2.THRESH_BINARY | cv2.THRESH_OTSU)[1]

elif args["preprocess"] == "blur":
    gray = cv2.medianBlur(gray, 3)

elif args["preprocess"] == "original":
    gray = cv2.medianBlur(gray, 1)


if args["extension"] == "png":
    filename = "{}.png".format(os.getpid())

cv2.imwrite(filename, gray)

text = image_to_string(Image.open(filename))
os.remove(filename)
print(text)

translated = Translator().translate(text, args["langcode"], 'en').text
cv2.imshow("Image", image)
cv2.imshow("Output", gray)

doc = docx.Document('doc.docx')
doc.add_paragraph(translated)
doc.save('doc.docx')
