import cv2


def draw_contours(src, cnts):
    """
    draw a list of contours on the origin image
    """
    for c in cnts:
        c.astype('int')
        cv2.drawContours(src, [c], -1, (0, 0, 255), 2)

    cv2.imshow('plate', src)
    cv2.waitKey()

def display_images(images_list, max_display_number):
    total_images = len(images_list)
    imgs_to_display = images_list[:max_display_number] if total_images > max_display_number else images_list
    for c in imgs_to_display:
        cv2.imshow(str(c), c)
    cv2.waitKey()
    cv2.destroyAllWindows()
