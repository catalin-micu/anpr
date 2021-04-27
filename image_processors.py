import cv2
import imutils
import numpy as np
import pytesseract


class ImageProcessor():
    def __init__(self, width):
        self.width = width
        self.raw_image = None
        self.gray_image = None
        self.blurred_image = None
        self.edge_image = None

    def read_image(self, path: str):
        """
        load the image for processing
        """
        img = cv2.imread(path)
        img = imutils.resize(img, width=self.width)
        self.raw_image = img

        return self.raw_image

    def turn_to_gray_and_blur(self, src, d, color, space):
        """
        apply grayscale filter and make the image smoother with blurring
        :param src: input image
        :param d: diameter of each pixel neighborhood that is used during filtering
        :param color: larger value = farther colors within the pixel neighborhood will be mixed together > larger areas
                                                                                            of semi-equal color
        :param space:  larger value = farther pixels will influence each other as long as their colors are close enough
        :return: smooth image
        """
        gray = cv2.cvtColor(src, cv2.COLOR_BGR2GRAY)
        self.gray_image = gray

        blurred = cv2.bilateralFilter(src=gray, d=d, sigmaColor=color, sigmaSpace=space)
        self.blurred_image = blurred

        return self.blurred_image

    def detect_edges(self, src, low_thresh, high_thresh):
        """
        finds the edges of the object in the image
        """
        edge = cv2.Canny(src, low_thresh, high_thresh)
        self.edge_image = edge

        return self.edge_image
