import numpy as np
import cv2
from PIL import Image
import pytesseract as tess


def draw_contours(src, cnts):
    """
    draw a list of contours on the origin image
    """
    for c in cnts:
        c.astype('int')
        cv2.drawContours(src, [c], -1, (0, 0, 255), 2)

    cv2.imshow('plate', src)
    cv2.waitKey()
