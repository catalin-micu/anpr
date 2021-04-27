import cv2
import imutils
import numpy as np
import pytesseract
from PIL import Image

import utils
from anpr import ANPR
from plate_detection import ShapeDetector
from image_processors import ImageProcessor

WIDTH = 72000
# possible scenarios

if __name__ == '__main__':
    ip = ImageProcessor(WIDTH)
    img = ip.read_image(path='images/plate4.jpg')
    # cv2.imshow('input', img)
    # cv2.waitKey()

    blurred = ip.turn_to_gray_and_blur(src=img, d=13, color=55, space=55)
    # cv2.imshow('blurred', blurred)
    # cv2.waitKey()

    edge = ip.detect_edges(src=blurred, low_thresh=30, high_thresh=150)
    cv2.imshow('edge', edge)
    cv2.waitKey()

    sd = ShapeDetector()
    contours = sd.get_contours(src=edge.copy())

    app_cnts = sd.approximate_contours(contours)
    poss_plates = sd.detect_possible_plates(app_cnts)
    utils.draw_contours(src=img.copy(), cnts=poss_plates)
    anpr = ANPR()
    cropped = anpr.crop_number_plate(blurred.copy(), poss_plates, img.copy())
    # for c in cropped:
    #     cv2.imshow(str(c), c)
    # cv2.waitKey()
    detected = anpr.detect_registration_number(cropped)

    for text in detected:
        print('Detected nb plate: ', text)
    cv2.waitKey()
