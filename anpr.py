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
        cleaned = re.sub(r'[^\dA-Z]', '', vrn)

        if re.match(r'^[A-Z]{2}', cleaned) and len(cleaned) == 7:
            if cleaned[2] == 'O':
                cleaned = cleaned[:2] + '0' + cleaned[3:]
            if cleaned[2] == 'I':
                cleaned = cleaned[:2] + '1' + cleaned[3:]
            if cleaned[3] == 'O':
                cleaned = cleaned[:3] + '0' + cleaned[4:]
            if cleaned[3] == 'I':
                cleaned = cleaned[:3] + '1' + cleaned[4:]

        if re.match(r'^B', cleaned) and len(cleaned) == 7:
            if cleaned[1] == 'O':
                cleaned = cleaned[:1] + '0' + cleaned[2:]
            if cleaned[1] == 'I':
                cleaned = cleaned[:1] + '1' + cleaned[2:]
            if cleaned[2] == 'O':
                cleaned = cleaned[:2] + '0' + cleaned[3:]
            if cleaned[2] == 'I':
                cleaned = cleaned[:2] + '1' + cleaned[3:]
            if cleaned[3] == 'O':
                cleaned = cleaned[:3] + '0' + cleaned[4:]
            if cleaned[3] == 'I':
                cleaned = cleaned[:3] + '1' + cleaned[4:]

        return cleaned


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
        for c in cropped_list:
            vrn = pytesseract.image_to_string(c, config='--psm 6')
            vrn = self.clean_number_plate(vrn)
            validated = self.validate_registration_number(vrn)
            if validated:
                return validated

        return None

    def crop(self, src, plates):
        cropped_plates = []
        for c in plates:
            x, y, w, h = cv2.boundingRect(c)
            cropped_plates.append(src[y:y+h, x:x+w])
        return cropped_plates
