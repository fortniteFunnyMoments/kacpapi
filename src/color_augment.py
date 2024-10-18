import cv2
import numpy as np

def grayscale(image, *args):
    print("image is", image)
    return cv2.cvtColor(image.get_original_image(), cv2.COLOR_BGR2GRAY)

def change_brightness(image, value):
    image = image.get_original_image()
    hsv = cv2.cvtColor(image, cv2.COLOR_BGR2HSV)
    h, s, v = cv2.split(hsv)

    v = cv2.add(v, value)
    v = np.clip(v, 0, 255)

    final_hsv = cv2.merge((h, s, v))
    brightened_image = cv2.cvtColor(final_hsv, cv2.COLOR_HSV2BGR)
    return brightened_image
