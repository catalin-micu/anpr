import re
import cv2
import numpy as np
import pytesseract

pytesseract.pytesseract.tesseract_cmd = r'C:\Program Files\Tesseract-OCR\tesseract.exe'


class ANPR():
    def __init__(self):
        self.cropped_sections = None

    def crop_number_plate(self, src, plates, raw_img):
        """
        crops a list of possible plates from the source image
        """
        mask = np.zeros(src.shape, np.uint8)
        cropped_sections = []
        for plate in plates:
            new_image = cv2.drawContours(mask, [plate], 0, 255, -1, )
            new_image = cv2.bitwise_and(raw_img, raw_img, mask=mask)
            (x, y) = np.where(mask == 255)
            (topx, topy) = (np.min(x), np.min(y))
            (bottomx, bottomy) = (np.max(x), np.max(y))
            cropped = src.copy()[topx:bottomx + 1, topy:bottomy + 1]

            cropped_sections.append(cropped)
        self.cropped_sections = cropped_sections

        return self.cropped_sections

    def clean_number_plate(self, vrn):
        """
        removes possible unwanted characters from the number
        """
        return re.sub(r'[^\dA-Z]', '', vrn)

    def validate_registration_number(self, vrn):
        """
        checks the format of the identified registration number
        """

    def detect_registration_number(self, cropped_list):
        detected = []
        for c in cropped_list:
            vrn = pytesseract.image_to_string(c, config='--psm 11')
            vrn = self.clean_number_plate(vrn)
            detected.append(vrn)

        return detected
