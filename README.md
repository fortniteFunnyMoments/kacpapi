# KACPAPI
KACPAPI is a Kivy application made to create pixel art and process images using opencv2 for image manipulation. This application is basically just a GUI frontend for a bunch of scripts I wrote while making pixel art images for games. Kivy application just loads available functions from a python dict and procedurally creates buttons, input fields, labels and such for them. KACPAPI supports loading in common image file types as well as loading in common video file types which are then saved a list of images to a user-specified directory. 
## Supported features
Currently, KACPAPI supports following image manipulation operations:
 - [x] Grayscale
 - [x] Pixelation (Image down-scaling)
 - [x] Changing image brightness
 - [x] Adding outline
	 - [ ] Changing outline color
 - [x] Applying custom color scheme
	 - [ ] Preloaded selection of color schemes 
 - [ ] Dithering
 - [ ] Better GUI
 - [ ] Builds for Android/Windows
These features work on both image and video files, however, saving modified video images is currently worked on. Some of these features may be WIP.
## Building
To build just install dependencies located in [reqs](reqs):

    python3 -m pip install -r reqs

and then run [app.py](app.py):

    python app.py
