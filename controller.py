import cv2
import utils
from anpr import ANPR
from image_processors import ImageProcessor
from plate_detection import ShapeDetector


class Controller():
    def __init__(self, img_width):
        self.IMAGE_WIDTH = img_width

    def run_edge_algorithm(self, blur_color, img_path):
        ip = ImageProcessor(self.IMAGE_WIDTH)
        img = ip.read_image(path=img_path)

        blurred = ip.turn_to_gray_and_blur(src=img, d=13, color=blur_color, space=55)  # plate 2 = 55 si chelutzu, plate4 = 25
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
        cropped = anpr.crop(src=blurred.copy(), plates=poss_plates)

        enhanced_cropped = anpr.enhance_cropped_plate(cropped)

        # utils.display_images(enhanced_cropped, 3)

        detected = anpr.detect_registration_number(enhanced_cropped)
        cv2.destroyAllWindows()

        return detected

    def run_otsu_algorithm(self, blur_color, img_path):
        ip = ImageProcessor(self.IMAGE_WIDTH)
        img = ip.read_image(path=img_path)

        blurred = ip.turn_to_gray_and_blur(src=img, d=13, color=blur_color, space=55)
        _, new = cv2.threshold(blurred.copy(), 0, 255, cv2.THRESH_BINARY + cv2.THRESH_OTSU)
        # cv2.imshow('blurred', blurred)
        # cv2.waitKey()

        edge = new
        cv2.imshow('edge', edge)
        cv2.waitKey()

        sd = ShapeDetector()
        contours = sd.get_contours(src=edge.copy())

        app_cnts = sd.approximate_contours(contours)
        poss_plates = sd.detect_possible_plates(app_cnts)
        utils.draw_contours(src=img.copy(), cnts=poss_plates)
        anpr = ANPR()
        cropped = anpr.crop(src=blurred.copy(), plates=poss_plates)

        enhanced_cropped = anpr.enhance_cropped_plate(cropped)

        # utils.display_images(enhanced_cropped, 3)

        detected = anpr.detect_registration_number(enhanced_cropped)
        cv2.destroyAllWindows()

        return detected

    def run(self, img_path):
        blurr_colors = [55, 45, 35, 25, 15, 5]
        for color in blurr_colors:
            result = self.run_otsu_algorithm(blur_color=color, img_path=img_path)
            if result:
                return result

        for color in blurr_colors:
            result = self.run_edge_algorithm(blur_color=color, img_path=img_path)
            if result:
                return result

        return None
