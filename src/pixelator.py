import cv2
import numpy as np
from src.image_manipulator import get_image_format

def change_image_scale(image, scale):
    scale = int(scale)
    print(image)
    width = int(image.shape[1] * scale / 100)
    height = int(image.shape[0] * scale / 100)
    print("changing image scale:", scale, "w:", width, "h:", height)
    scaled_image = cv2.resize(image, (width, height), interpolation=cv2.INTER_AREA)
    return scaled_image

def add_outline(image, *args):
    img_format, _ = get_image_format(image)
    
    if img_format == 'bgr':  # Convert to grayscale before detecting edges
        gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    elif img_format == 'grayscale':
        gray = image  # Already grayscale
    else:
        raise ValueError("Unsupported image format for add_outline")

    outline = detect_edges(gray)
    outline = np.where(outline > 127, 255, 0).astype(np.uint8)
    combined = np.where(outline == 255, 255, gray)
    return combined

def dithering(image, *args):
    img_format, _ = get_image_format(image)
    
    if img_format == 'bgr':  # Convert to grayscale for dithering
        gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    elif img_format == 'grayscale':
        gray = image
    else:
        raise ValueError("Unsupported image format for dithering")
    
    output = gray.copy().astype(np.float32)
    # Dithering algorithm...
    return output

def shift_edges(edges, dx, dy):
    translation_matrix = np.float32([[1, 0, dx], [0, 1, dy]])
    shifted_edges = cv2.warpAffine(edges, translation_matrix, (edges.shape[1], edges.shape[0]))
    return shifted_edges

def detect_edges(image): #image has to be grayscale
    edges = cv2.Canny(image, 100, 200)
    print("detect edges edges:", edges)
    return edges
