# import os for saving
import os

# import image and video handler logic
from src.image_manipulator import ImageManipulator
import src.video_manipulator as vidman

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
from kivy.uix.checkbox import CheckBox
from kivy.uix.image import Image
from kivy.uix.slider import Slider
from kivy.uix.textinput import TextInput
from kivy.uix.filechooser import FileChooserListView
from kivy.graphics.texture import Texture

class FrameRatePopup(Popup):
    def __init__(self, frame_rate_callback, **kwargs):
        super(FrameRatePopup, self).__init__(**kwargs)
        self.title = 'Select Frame Rate'
        self.size_hint = (0.9, 0.4)

        layout = BoxLayout(orientation='vertical')
        self.frame_rate_input = TextInput(hint_text="Enter frame rate (N)", multiline=False, size_hint_y=None, height=40)
        layout.add_widget(self.frame_rate_input)

        button_layout = BoxLayout(size_hint_y=None, height=50)
        select_button = Button(text="OK", on_press=self.select_frame_rate)
        cancel_button = Button(text="Cancel", on_press=self.dismiss)

        button_layout.add_widget(select_button)
        button_layout.add_widget(cancel_button)
        layout.add_widget(button_layout)
        self.content = layout

        self.frame_rate_callback = frame_rate_callback

    def select_frame_rate(self, instance):
        try:
            n = int(self.frame_rate_input.text.strip())
            self.dismiss()
            self.frame_rate_callback(n)
        except ValueError:
            print("Please enter a valid integer.")

class SaveFilePopup(Popup):
    def __init__(self, save_callback, **kwargs):
        super(SaveFilePopup, self).__init__(**kwargs)
        self.title = 'Save Image As'
        self.size_hint = (0.9, 0.9)

        self.selected_directory = None
        
        layout = BoxLayout(orientation='vertical', spacing=10)
        
        self.filechooser = FileChooserListView(dirselect=True)
        self.filechooser.bind(selection=self.update_selected_directory)
        layout.add_widget(self.filechooser)

        # this needs to append .jpg or .png automatically
        self.filename_input = TextInput(hint_text="Enter filename (e.g., image.png)DONT FORGET .png OR .jpg!", multiline=False, size_hint_y=None, height=40)
        layout.add_widget(self.filename_input)
        
        button_layout = BoxLayout(size_hint_y=None, height=50)
        save_button = Button(text="Save", on_press=lambda *args: self.save(save_callback))
        cancel_button = Button(text="Cancel", on_press=self.dismiss)
        
        button_layout.add_widget(save_button)
        button_layout.add_widget(cancel_button)
        layout.add_widget(button_layout)
        
        self.content = layout

    def update_selected_directory(self, filechooser, selection):
        print("selection happened", selection)
        if selection:
            selected_path = selection[0]
            if os.path.isdir(selected_path):
                self.selected_directory = selected_path
            else:                
                self.selected_directory = filechooser.path

    def save(self, save_callback):
        directory = self.selected_directory
        filename = self.filename_input.text.strip()

        if not directory:
            print("Please select a directory.")
            return
        if not filename:
            print("Please enter a filename.")
            return
        
        file_path = os.path.join(directory, filename)
        self.dismiss()
        
        save_callback(file_path)

class FilePickerPopup(Popup):
    def __init__(self, **kwargs):
        super(FilePickerPopup, self).__init__(**kwargs)
        self.title = 'Select an Image or Video'
        self.size_hint = (0.9, 0.9)

        layout = BoxLayout(orientation='vertical')
        self.filechooser = FileChooserListView(filters=['*.png', '*.jpg', '*.jpeg', '*.mp4', '*.avi', '*.mov'])
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
            file_path = selected[0]
            self.dismiss()
            if file_path.endswith(('.mp4', '.avi', '.mov')):  
                frame_rate_popup = FrameRatePopup(lambda n: App.get_running_app().root.load_video(n, file_path))
                frame_rate_popup.open()
            else:
                App.get_running_app().root.load_file(file_path)

    def on_frame_rate_selected(self, frame_rate):
        App.get_running_app().root.load_video(frame_rate)
        
    
class MainApp(BoxLayout):
    def __init__(self, **kwargs):
        super(MainApp, self).__init__(**kwargs)
        self.orientation = 'vertical'

        self.kacpapi_function_map = {
            "dithering":pxl.dithering,
            "change_scale":pxl.change_image_scale,
            #"detect_edges":pxl.detect_edges,
            #"shift_edges":pxl.shift_edges,
            "add_outline":pxl.add_outline,

            "grayscale":cagm.grayscale,
            "brightness":cagm.change_brightness,
            "apply_color_scheme":cagm.apply_color_scheme
            }

        img_comparator = BoxLayout(orientation = 'horizontal')
        self.original_image = Image(allow_stretch=True, size_hint_y=None, height=300)
        self.augmented_image = Image(allow_stretch=True, size_hint_y=None, height=300)
        self.label = Label(text="No file selected", size_hint_y=None, height=50)

        self.augmented_image.bind(texture=self.on_texture_load)
        self.original_image.bind(texture=self.on_texture_load)
        
        img_comparator.add_widget(self.original_image)
        img_comparator.add_widget(self.augmented_image)
        self.add_widget(self.label)
        self.add_widget(img_comparator)

        self.browse_buttons = BoxLayout(orientation='horizontal', size_hint_y=None, height=50)
        self.prev_button = Button(text="<", on_press=self.previous_frame, disabled=True)
        self.next_button = Button(text=">", on_press=self.next_frame, disabled=True)
        self.browse_buttons.add_widget(self.prev_button)
        self.browse_buttons.add_widget(self.next_button)
        self.add_widget(self.browse_buttons)

        general_img_operator = BoxLayout(orientation = 'horizontal')
        
        file_button = Button(text="Select Image/Video", size_hint_y=None, height=50)
        file_button.bind(on_press=self.open_file_picker)
        revert_button = Button(text="Revert changes", size_hint_y=None, height=50)
        revert_button.bind(on_press=self.revert_img)
        save_button = Button(text="Save image", size_hint_y=None, height=50)
        save_button.bind(on_press=self.save_img)
        
        general_img_operator.add_widget(file_button)
        general_img_operator.add_widget(revert_button)
        general_img_operator.add_widget(save_button)

        self.add_widget(general_img_operator)
        
        self.generate_widgets()
                
        self.image_handler = None
        self.load_file("data/example_data/example_img.jpg")


    def generate_widgets(self):
        for func_name in self.kacpapi_function_map:
            augment_widget_box = BoxLayout(orientation='horizontal', size_hint_y=None, height=50)
            function_label = Label(text=func_name)
            augment_button = Button(text="Test")
            text_input = TextInput(hint_text=func_name.capitalize(), size_hint_x=0.6, multiline=False)
            apply_button =  Button(text="Apply permanently", size_hint_x=0.4)

            augment_button.bind(on_press=self.create_button_callback(func_name, text_input))
            apply_button.bind(on_press=self.apply_augment)

            augment_widget_box.add_widget(function_label)
            augment_widget_box.add_widget(augment_button)
            augment_widget_box.add_widget(text_input)
            augment_widget_box.add_widget(apply_button)

            self.add_widget(augment_widget_box)

    def create_button_callback(self, func_name, text_input):
        def button_callback(instance):
            if text_input.text != "":
                value = text_input.text #this should be made more robust
            else:
                value = 0
            print("btn callback value:", value)
            self.apply_augmentation(func_name, value)
        return button_callback

    def apply_augmentation(self, func_name, *args):
        if self.image_handler is not None:
            img = self.image_handler.get_image()  # This should return a NumPy array
            func = self.kacpapi_function_map.get(func_name)
            print("apply_augmentation - function:", func, "img:", img, "with arguments:", *args)
            if func:
                augmented_img = func(img, *args)
                self.image_handler.img = augmented_img
                self.display_image(self.image_handler.get_image(), self.augmented_image)

    def open_file_picker(self, instance):
        file_picker = FilePickerPopup()
        file_picker.open()

    def revert_img(self, instance):
        if self.image_handler is not None:
            curr_img = self.image_handler.get_image()         
            og_img = self.image_handler.get_original_image()
            print("reverting to:", og_img, "from:", curr_img)
            texture = self.image_handler.display_image(og_img)
            self.augmented_image.texture = texture
        else:
            print("no image selected!")
        print("now augmented image is:", self.augmented_image.texture)
        
    def save_img(self, instance):
        # Open the SaveFilePopup, passing the save_image method as a callback
        save_popup = SaveFilePopup(self.save_image_to_path)
        save_popup.open()

    # Callback to save the image at the specified path
    def save_image_to_path(self, path):
        # Ensure path has an extension
        if not path.endswith(('.jpg', '.png')):
            path += '.png'  # Default to PNG if no extension is given
        if self.image_handler is not None:
            print(f"Saving image to {path}")
            self.image_handler.save_image(path)
        else:
            print("No image loaded to save.")

    def apply_augment(self, instance):
        if self.image_handler is not None:
            image_to_apply = self.augmented_image.texture
            print("applying something to", image_to_apply)
            self.image_handler.texture_to_image(image_to_apply)
        self.display_image(self.image_handler.get_image(), self.augmented_image)
        
    def load_file(self, file_path):
        self.image_handler = ImageManipulator(file_path)
        self.display_image(self.image_handler.get_image(), self.original_image)
        self.label.text = f"Selected File: {file_path}"

    def load_video(self, n, path):
        print("n:", n, "path:", path)
        #frame_rate_popup = FrameRatePopup(self.extract_frames(n, path))
        self.extract_frames(n, path)
        #frame_rate_popup.open()

    def extract_frames(self, n, path):
        raw_frames = vidman.get_frames_from_video(path, n)
        self.video_frames = [ImageManipulator() for _ in raw_frames]  #create image manipulators 

        for i, frame in enumerate(raw_frames):
            self.video_frames[i].img = frame
            
        self.current_frame_index = 0

        if self.video_frames:
            # Use the existing display_image method
            self.display_image(self.video_frames[self.current_frame_index].get_image(), self.original_image)  # Display the first frame
            self.prev_button.disabled = False
            self.next_button.disabled = False
            self.label.text = f"Extracted {len(self.video_frames)} frames."
        else:
            self.label.text = "No frames extracted."
            
    def previous_frame(self, instance):
        if self.video_frames and self.current_frame_index > 0:
            self.current_frame_index -= 1
            self.change_frame(self.current_frame_index)

    def next_frame(self, instance):
        if self.video_frames and self.current_frame_index < len(self.video_frames) - 1:
            self.current_frame_index += 1
            self.change_frame(self.current_frame_index)

    def change_frame(self, idx):
        #self.new_img = self.video_frames[idx].get_image()
        #self.image_handler = self.new_img
        #self.image_handler.set_image(self.new_img)
        self.image_handler = self.video_frames[idx]
        self.display_image(self.image_handler.get_image(), self.original_image)
        
        
            
    def display_image(self, img, image_widget):
        if self.image_handler is not None:
            texture = self.image_handler.display_image(img)
            image_widget.texture = texture
            
    def on_texture_load(self, instance, texture):
        instance.texture.min_filter = 'nearest'
        instance.texture.mag_filter = 'nearest'
        
class MyKivyApp(App):
    def build(self):
        #self.icon = "data/"
        return MainApp()

if __name__ == '__main__':
    MyKivyApp().run()
