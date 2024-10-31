import cv2
import numpy as np
from kivy.graphics.texture import Texture

def get_image_format(image):
    if len(image.shape) == 2:  # Grayscale images have two dimensions (height, width)
        return 'grayscale', 1
    elif len(image.shape) == 3 and image.shape[2] == 3:  # Color images with 3 channels (BGR)
        return 'bgr', 3
    elif len(image.shape) == 3 and image.shape[2] == 4:  # Images with 4 channels (RGBA)
        return 'rgba', 4
    else:
        raise ValueError("Unknown image format.")

class ImageManipulator:

    def __init__(self, path=None):
        self.img = None
        self.original_img = None
        if path:
            self.set_image(path)        

    def texture_to_image(self, texture):
        pixel_data = texture.pixels
        width, height = texture.size
        colorfmt = texture.colorfmt

        print(f"Texture size: {width}x{height}")
        print(f"Color format: {colorfmt}")
        print(f"Length of pixel data: {len(pixel_data)}")

        if colorfmt == 'rgba':
            channels = 4
        elif colorfmt == 'rgb' or colorfmt == 'bgr':
            channels = 3
        elif colorfmt == 'luminance':
            channels = 1
        else:
            raise ValueError(f"Unsupported color format: {colorfmt}")
        
        expected_size = width * height * channels
        print(f"Expected size of pixel data: {expected_size}")
        pixel_data = pixel_data[:expected_size]  # Truncate if larger
        new_img = np.frombuffer(pixel_data, dtype=np.uint8).reshape((height, width, channels))
        
        if colorfmt == 'rgba':
            new_img = np.frombuffer(pixel_data, dtype=np.uint8).reshape((height, width, 4))
            new_img = cv2.cvtColor(new_img, cv2.COLOR_RGBA2BGR)
        elif colorfmt == 'rgb':
            new_img = np.frombuffer(pixel_data, dtype=np.uint8).reshape((height, width, 3))
            new_img = cv2.cvtColor(new_img, cv2.COLOR_RGB2BGR)
        elif colorfmt == 'bgr':
            new_img = np.frombuffer(pixel_data, dtype=np.uint8).reshape((height, width, 3))
        elif colorfmt == 'luminance':
            new_img = np.frombuffer(pixel_data, dtype=np.uint8).reshape((height, width))
            new_img = cv2.cvtColor(new_img, cv2.COLOR_GRAY2BGR)
        else:
            raise ValueError(f"Unsupported color format: {colorfmt}")

        new_img = cv2.flip(new_img, 0)
        self.img = new_img
            
    def set_image(self, path):
        self.img = cv2.imread(path)
        if self.img is None:
            raise FileNotFoundError(f"Image at {path} could not be loaded.")
        self.original_img = self.img.copy()
    
    def get_image(self):
        return self.img

    def save_image(self, path):
        if self.img is not None:
            cv2.imwrite(path, self.img)
        else:
            raise ValueError("No image to save.")

    def display_image(self, img):
        if img is not None:
            if len(img.shape) == 2:  # Grayscale image
                # Convert grayscale to a 3-channel image (BGR) for displaying in Kivy
                display_img = cv2.cvtColor(img, cv2.COLOR_GRAY2BGR)
            else:
                display_img = img

            buffer = cv2.flip(display_img, 0).tobytes()
            texture = Texture.create(size=(img.shape[1], img.shape[0]), colorfmt='bgr')
            texture.blit_buffer(buffer, colorfmt='bgr', bufferfmt='ubyte')
            return texture
        else:
            raise ValueError("No image loaded to display.")
    
    def get_original_image(self):
        return self.original_img
