# import image handler logic
from src.image_manipulator import ImageManipulator

# import actual logic
import src.pixelator as pxl
import src.color_augment as cagm

# import kivy
import kivy
from kivy.app import App
from kivy.uix.label import Label
from kivy.uix.popup import Popup
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.button import Button
from kivy.uix.image import Image
from kivy.uix.slider import Slider
from kivy.uix.filechooser import FileChooserListView
from kivy.graphics.texture import Texture

class FilePickerPopup(Popup):
    def __init__(self, **kwargs):
        super(FilePickerPopup, self).__init__(**kwargs)
        self.title = 'Select an Image or Video'
        self.size_hint = (0.9, 0.9)

        layout = BoxLayout(orientation='vertical')
        self.filechooser = FileChooserListView(filters=['*.png', '*.jpg', '*.jpeg', '*.mp4'])
        layout.add_widget(self.filechooser)

        button_layout = BoxLayout(size_hint_y=None, height=50)
        select_button = Button(text="Select", on_press=self.select_file)
        cancel_button = Button(text="Cancel", on_press=self.dismiss)

        button_layout.add_widget(select_button)
        button_layout.add_widget(cancel_button)
        layout.add_widget(button_layout)
        self.content = layout

    def select_file(self, instance):
        selected = self.filechooser.selection
        if selected:
            self.dismiss()
            App.get_running_app().root.load_file(selected[0])
    
class MainApp(BoxLayout):
    def __init__(self, **kwargs):
        super(MainApp, self).__init__(**kwargs)
        self.orientation = 'vertical'

        # Image widgets to show original and augmented images
        self.original_image = Image(allow_stretch=True, size_hint_y=None, height=300)
        self.augmented_image = Image(allow_stretch=True, size_hint_y=None, height=300)
        self.label = Label(text="No file selected", size_hint_y=None, height=50)

        self.augmented_image.bind(texture=self.on_texture_load)
        self.original_image.bind(texture=self.on_texture_load)
        
        # Add widgets to the layout
        self.add_widget(self.original_image)
        self.add_widget(self.augmented_image)
        self.add_widget(self.label)

        # File selection button
        file_button = Button(text="Select Image/Video", size_hint_y=None, height=50)
        file_button.bind(on_press=self.open_file_picker)
        self.add_widget(file_button)

        # Buttons for applying augmentations
        grayscale_button = Button(text="Apply Grayscale", size_hint_y=None, height=50)
        grayscale_button.bind(on_press=self.apply_grayscale)
        self.add_widget(grayscale_button)

        # Slider for brightness adjustment
        self.brightness_slider = Slider(min=-100, max=100, value=0, size_hint_y=None, height=50)
        self.brightness_slider.bind(value=self.apply_brightness)
        self.add_widget(Label(text="Adjust Brightness", size_hint_y=None, height=50))
        self.add_widget(self.brightness_slider)

        # Slider for scaling
        self.downscale_slider = Slider(min=1, max=10, value=5, size_hint_y=None, height=50)
        self.downscale_slider.bind(value=self.apply_scale)
        self.add_widget(Label(text="Downscale Image", size_hint_y=None, height=50))
        self.add_widget(self.downscale_slider)

        self.image_handler = None

    def open_file_picker(self, instance):
        file_picker = FilePickerPopup()
        file_picker.open()

    def load_file(self, file_path):
        self.image_handler = ImageManipulator(file_path)
        self.display_image(self.image_handler.get_image(), self.original_image)
        self.label.text = f"Selected File: {file_path}"

    def display_image(self, img, image_widget):
        if self.image_handler is not None:
            texture = self.image_handler.display_image()
            image_widget.texture = texture

    def apply_grayscale(self, instance):
        if self.image_handler is not None:
            img = self.image_handler.get_image()
            self.image_handler.img = cagm.grayscale(img)
            self.display_image(self.image_handler.get_image(), self.augmented_image)

    # when grayscale throws error: invalid number of channels in input image scn is 1
    def apply_brightness(self, instance, value):
        if self.image_handler is not None:
            img = self.image_handler.get_image()
            self.image_handler.img = cagm.change_brightness(img, value)
            self.display_image(self.image_handler.get_image(), self.augmented_image)

    def apply_scale(self, instance, value):
        if self.image_handler is not None:
            img = self.image_handler.get_image()
            self.image_handler.img = pxl.change_image_scale(img, value)
            self.display_image(self.image_handler.get_image(), self.augmented_image)
    def on_texture_load(self, instance, texture):
        instance.texture.min_filter = 'nearest'
        instance.texture.mag_filter = 'nearest'
        
class MyKivyApp(App):
    def build(self):
        return MainApp()

if __name__ == '__main__':
    MyKivyApp().run()
