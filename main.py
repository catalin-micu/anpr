import cv2
import imutils
import numpy as np
import pytesseract
from PIL import Image

import utils
from anpr import ANPR
from controller import Controller
from plate_detection import ShapeDetector
from image_processors import ImageProcessor

WIDTH = 720
# possible scenarios

if __name__ == '__main__':
    controller = Controller(WIDTH)
    detected_registration_number = controller.run(img_path='images/chelutzu.jpg')

    if detected_registration_number:
        print('Detected number plate:', detected_registration_number)
    else:
        print('No number plate detected.')
    cv2.waitKey()

