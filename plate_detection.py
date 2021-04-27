import cv2
import imutils


class ShapeDetector:
    def __init__(self):
        self.plate_found = False
        self.contours = None
        self.approx_contours = None
        self.possible_plates = None

    def get_contours(self, src):
        """
        extracts only the closed contours in the image
        contour =  any curve in the image
        """
        contours = cv2.findContours(src, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)
        contours = imutils.grab_contours(contours)
        contours = sorted(contours, key=cv2.contourArea, reverse=True)
        self.contours = contours

        return self.contours

    def approximate_contours(self, contours):
        """
        minimize contour data points
        """
        approx_contours = []

        for c in contours:
            peri = cv2.arcLength(c, True)
            approx = cv2.approxPolyDP(c, 0.018 * peri, True)
            approx_contours.append(approx)

        self.approx_contours = approx_contours

        return self.approx_contours


    def check_rectangle_ratio(self, w, h) -> bool:
        """
        check if a rectangle respects the ratio of a Romanian licence plate
        """
        aspect_ratio = w / float(h)
        # print(aspect_ratio)
        # print(w)
        # print(h)
        if 4 < aspect_ratio < 6:
            return True
        return False

    def detect_possible_plates(self, approx_list):
        """
        keep only the rectangle contours
        """
        possible_plate_list = []

        for approx in approx_list:
            if len(approx) == 4:
                (x, y, w, h) = cv2.boundingRect(approx)

                if self.check_rectangle_ratio(w, h):
                    possible_plate_list.append(approx)

        self.possible_plates = possible_plate_list

        return self.possible_plates
