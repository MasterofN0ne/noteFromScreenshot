from PIL import Image
import pytesseract
import os
import cv2 
import numpy as np


pytesseract.pytesseract.tesseract_cmd = r'/usr/local/bin/tesseract'




def clear_img(filename):
    img = cv2.imread(filename)
    img = cv2.resize(img, None, fx=1.2, fy=1.2, interpolation=cv2.INTER_CUBIC)
    img = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)

    kernel = np.ones((1, 1), np.uint8)
    img = cv2.dilate(img, kernel, iterations=1)
    img = cv2.erode(img, kernel, iterations=1)

    cv2.threshold(cv2.GaussianBlur(img, (5, 5), 0), 0, 255, cv2.THRESH_BINARY + cv2.THRESH_OTSU)[1]

    cv2.threshold(cv2.bilateralFilter(img, 5, 75, 75), 0, 255, cv2.THRESH_BINARY + cv2.THRESH_OTSU)[1]

    cv2.threshold(cv2.medianBlur(img, 3), 0, 255, cv2.THRESH_BINARY + cv2.THRESH_OTSU)[1]

    cv2.adaptiveThreshold(cv2.GaussianBlur(img, (5, 5), 0), 255, cv2.ADAPTIVE_THRESH_GAUSSIAN_C, cv2.THRESH_BINARY, 31, 2)

    cv2.adaptiveThreshold(cv2.bilateralFilter(img, 9, 75, 75), 255, cv2.ADAPTIVE_THRESH_GAUSSIAN_C, cv2.THRESH_BINARY, 31, 2)

    cv2.adaptiveThreshold(cv2.medianBlur(img, 3), 255, cv2.ADAPTIVE_THRESH_GAUSSIAN_C, cv2.THRESH_BINARY, 31, 2)
    
    cv2.imwrite(filename, img)


def extractNotes():
    dir = 'assets/week5'
    file = open("histnotes_week_6_7_8.txt", "w")
    counter = 1
    for filename in os.listdir("week6-7-8"):
        print(counter)
        if filename.endswith(".png"):
            clear_img(f"week6-7-8/{filename}")
            text = pytesseract.image_to_string(Image.open(f"week6-7-8/{filename}"), lang='tur')
            file.write(f"Extracted from {filename} file..\n")
            file.write(text)
            file.write("-----------------------------------------------------------------\n")
            counter += 1 
    

    file.close()

extractNotes()
