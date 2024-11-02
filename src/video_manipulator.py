import cv2

def get_frames_from_video(video_path, n):
        frames = []
        cam = cv2.VideoCapture(video_path)
        
        if not cam.isOpened():
            print("Error: Could not open video.")
            return frames
        
        frame_count = 0
        
        while True:
            ret, frame = cam.read()
            if not ret:
                break
            
            if frame_count % n == 0:
                frames.append(frame)
            
            frame_count += 1

        cam.release()
        return frames
