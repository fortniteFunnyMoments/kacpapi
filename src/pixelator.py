import cv2

def change_image_scale(image, scale):
    if scale < 0:
        scale = 0.5 ** abs(scale)
    if scale == 0:
        scale = 1
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
    return edges

def add_outline(image, outline):
    outline = np.where(outline > 127, 255, 0).astype(np.uint8)
    combined = np.where(outline == 255, 255, image)
    return combined

