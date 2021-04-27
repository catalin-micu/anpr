import re
import cv2
import numpy as np
import pytesseract

pytesseract.pytesseract.tesseract_cmd = r'C:\Program Files\Tesseract-OCR\tesseract.exe'


class ANPR():
    def __init__(self):
        self.cropped_sections = None
        self.enhanced_cropped_sections = None
        self.COUNTRY_REGULAR_PLATE = r'[A-Z]{2}\d{2}[A-Z]{3}'
        self.BUC_REGULAR_PLATE = r'B\d{2,3}[A-Z]{3}'
        self.COUNTRY_TEMPORARY_PLATE = r'[A-Z]{2}\d{6}'
        self.BUC_TEMPORARY_PLATE = r'B\d{6}'

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

    def enhance_cropped_plate(self, cropped):
        """
        applies some image processing on cropped plates before detecting the text
        """
        enhanced_cropped = []
        for c in cropped:
            new = cv2.GaussianBlur(c, (5, 5), 0)
            _, new = cv2.threshold(new, 0, 255, cv2.THRESH_BINARY + cv2.THRESH_OTSU)
            enhanced_cropped.append(new)

        self.enhanced_cropped_sections = enhanced_cropped

        return self.enhanced_cropped_sections

    def clean_number_plate(self, vrn):
        """
        removes possible unwanted characters from the number
        """
        return re.sub(r'[^\dA-Z]', '', vrn)

    def validate_registration_number(self, vrn):
        """
        checks the format of the identified registration number
        """
        reg_plate_cases = [self.COUNTRY_REGULAR_PLATE, self.BUC_REGULAR_PLATE, self.COUNTRY_TEMPORARY_PLATE,
                           self.BUC_TEMPORARY_PLATE]
        for reg_exp in reg_plate_cases:
            r = re.compile(reg_exp)
            res = r.search(vrn)
            if res:
                return res.group()

        return None

    def detect_registration_number(self, cropped_list):
        detected = []
        for c in cropped_list:
            vrn = pytesseract.image_to_string(c, config='--psm 6')
            vrn = self.clean_number_plate(vrn)
            detected.append(vrn)

        return detected
