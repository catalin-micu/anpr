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
    img = ip.read_image(path='images/plate2.jpg')
    # cv2.imshow('input', img)
    # cv2.waitKey()

    blurred = ip.turn_to_gray_and_blur(src=img, d=13, color=55, space=55)  # plate 2 = 55 si chelutzu, plate4 = 25
    # _, new = cv2.threshold(blurred.copy(), 0, 255, cv2.THRESH_BINARY + cv2.THRESH_OTSU)
    # cv2.imshow('blurred', blurred)
    # cv2.waitKey()

    edge = ip.detect_edges(src=blurred, low_thresh=30, high_thresh=150)
    # edge = new
    cv2.imshow('edge', edge)
    cv2.waitKey()

    sd = ShapeDetector()
    contours = sd.get_contours(src=edge.copy())

    app_cnts = sd.approximate_contours(contours)
    poss_plates = sd.detect_possible_plates(app_cnts)
    utils.draw_contours(src=img.copy(), cnts=poss_plates)
    anpr = ANPR()
    cropped = anpr.crop(src=blurred.copy(), plates=poss_plates, raw_img=img.copy())

    enhanced_cropped = anpr.enhance_cropped_plate(cropped)

    # for c in enhanced_cropped:
    #     cv2.imshow(str(c), c)
    # cv2.waitKey()

    detected = anpr.detect_registration_number(enhanced_cropped)

    validated = None
    for text in detected:
        validated = anpr.validate_registration_number(text)
        if validated:
            break

    if validated:
        print('Detected number plate:', validated)
    else:
        print('No number plate detected.')
    cv2.waitKey()

    # stop printing all the cropped plates
    # implement the dynamic blurring and increase speed by validating withing the process
