import cv2
import numpy as np
import math
from src.image_manipulator import get_image_format 

def grayscale(image, *args):
    img_format, _ = get_image_format(image)
    
    if img_format == 'bgr':
        return cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    elif img_format == 'grayscale':
        return image
    else:
        raise ValueError("Unsupported image format for grayscale conversion")

def change_brightness(image, value):
    img_format, _ = get_image_format(image)
    value = int(value)
    print("change brightness val", value)
    
    if img_format == 'bgr':
        hsv = cv2.cvtColor(image, cv2.COLOR_BGR2HSV)
        h, s, v = cv2.split(hsv)

        v = cv2.add(v, value)
        v = np.clip(v, 0, 255)

        final_hsv = cv2.merge((h, s, v))
        brightened_image = cv2.cvtColor(final_hsv, cv2.COLOR_HSV2BGR)
        return brightened_image
    elif img_format == 'grayscale':
        brightened_image = cv2.add(image, value)
        return np.clip(brightened_image, 0, 255)
    else:
        raise ValueError("Unsupported image format for brightness adjustment")

def apply_color_scheme(image, scheme):
    img_format, _ = get_image_format(image)
    
    if img_format == 'bgr':
        color_array = []
        for color in scheme.split():
            rgb_color = tuple(int(color[i:i+2], 16) for i in (0, 2, 4))
            color_array.append(rgb_color)
        for i in range(image.shape[0]):
            for j in range(image.shape[1]):            
                pixel_rgb = tuple(image[i, j][:3])    
                closest_color = find_closest_color(pixel_rgb, color_array)
                image[i, j][:3] = closest_color
    else:
        print("image has no color!")        
    return image
    
def find_closest_color(pixel_rgb, palette_rgb):
    closest_color = palette_rgb[0]
    min_distance = euclidean_distance(pixel_rgb, closest_color)
    
    for color in palette_rgb[1:]:
        distance = euclidean_distance(pixel_rgb, color)
        if distance < min_distance:
            min_distance = distance
            closest_color = color
    
    return closest_color

def euclidean_distance(color1, color2):
    return math.sqrt(sum((comp1 - comp2) ** 2 for comp1, comp2 in zip(color1, color2)))
