import cv2
import numpy as np

def change_image_scale(image, scale):
    #image = image.get_image()
    print(image)
    width = int(image.shape[1] * scale / 100)
    height = int(image.shape[0] * scale / 100)
    print("changing image scale:", scale, "w:", width, "h:", height)
    scaled_image = cv2.resize(image, (width, height), interpolation=cv2.INTER_AREA)
    return scaled_image

def shift_edges(edges, dx, dy):
    translation_matrix = np.float32([[1, 0, dx], [0, 1, dy]])
    shifted_edges = cv2.warpAffine(edges, translation_matrix, (edges.shape[1], edges.shape[0]))
    return shifted_edges

def detect_edges(image): #image has to be grayscale
    edges = cv2.Canny(image, 100, 200)
    print("detect edges edges:", edges)
    return edges

def add_outline(image, *args): #image has to be grayscale
    #image = image.get_original_image()
    gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    if len(image.shape) == 2:
        print("is grayscale")
        outline = detect_edges(image)
    else:
        outline = detect_edges(gray)
    outline = np.where(outline > 127, 255, 0).astype(np.uint8)
    combined = np.where(outline == 255, 255, gray)
    print("add outline:", outline)
    return combined

def dithering(image, *args): #atkinson's algorithm
    #image = image.get_image()
    
    gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    output = gray.copy().astype(np.float32)
    
    atkinson_filter = np.array([[0, 0, 1, 1],
                                [1, 1, 1, 0],
                                [0, 1, 0, 0]], dtype=np.float32) / 8.0

    rows, cols = output.shape
    for y in range(rows):
        for x in range(cols):
            old_pixel = output[y, x]
            new_pixel = 255 if old_pixel > 127 else 0 #adjust this 127 if too dark
            output[y, x] = new_pixel
            quant_error = old_pixel - new_pixel
            
            for dy in range(3):
                for dx in range(4):
                    ny, nx = y + dy - 1, x + dx - 1
                    if 0 <= ny < rows and 0 <= nx < cols:
                        output[ny, nx] += quant_error * atkinson_filter[dy, dx]

    output = np.where(output > 127, 255, 0).astype(np.uint8) # convert to bin
    # save as image
    return output
