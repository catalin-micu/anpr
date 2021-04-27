import cv2
import imutils
import numpy as np
import pytesseract
from PIL import Image

import utils
from anpr import ANPR
from plate_detection import ShapeDetector
from image_processors import ImageProcessor

WIDTH = 720
# possible scenarios

if __name__ == '__main__':
    ip = ImageProcessor(WIDTH)
    img = ip.read_image(path='images/plate1.jpg')
    # cv2.imshow('input', img)
    # cv2.waitKey()

    blurred = ip.turn_to_gray_and_blur(src=img, d=13, color=25, space=55)  # plate 2 are nev de 55
    # cv2.imshow('blurred', blurred)
    # cv2.waitKey()

    edge = ip.detect_edges(src=blurred, low_thresh=30, high_thresh=150)
    # cv2.imshow('edge', edge)
    # cv2.waitKey()

    sd = ShapeDetector()
    contours = sd.get_contours(src=edge.copy())

    app_cnts = sd.approximate_contours(contours)
    poss_plates = sd.detect_possible_plates(app_cnts)
    # utils.draw_contours(src=img.copy(), cnts=poss_plates)
    anpr = ANPR()
    cropped = anpr.crop_number_plate(src=blurred.copy(), plates=poss_plates, raw_img=img.copy())

    enhanced_cropped = anpr.enhance_cropped_plate(cropped)

    for c in enhanced_cropped:
        cv2.imshow(str(c), c)
    cv2.waitKey()

    detected = anpr.detect_registration_number(enhanced_cropped)

    for text in detected:
        validated = anpr.validate_registration_number(text)
        if validated:
            break

    print('Detected number plate:', validated)
    cv2.waitKey()

    # stop printing all the cropped plates
    # try to fix chelutzu, else implement the dynamic blurring and increase speed by validating withing the process
