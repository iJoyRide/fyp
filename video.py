import cv2
import os
import time
import logging
from ultralytics import YOLO
from object_classes import classNames

# Configure logging
logging.basicConfig(level=logging.INFO)

# Function to capture images for a specific duration
def capture_images(duration, subfolder_path, classNames, video_path):
    try:
        # Open the video file
        cap = cv2.VideoCapture(video_path)
        if not cap.isOpened():
            logging.error(f"Failed to open video file: {video_path}")
            return
        
        start_time = time.time()
        while time.time() - start_time < duration:
            success, img = cap.read()
            if not success:
                logging.error("Failed to capture image from video.")
                break
            
            results = model(img, stream=True)
            
            for r in results:
                boxes = r.boxes
                for box in boxes:
                    x1, y1, x2, y2 = map(int, box.xyxy[0])
                    cls = int(box.cls[0])
                    confidence = box.conf[0]  # Extract confidence score
                    # Object details
                    org = [x1, y1]
                    font = cv2.FONT_HERSHEY_SIMPLEX
                    fontScale = 1
                    color = (0, 255, 0)  # Change color to green
                    thickness = 1

                    if cls == 0:
                        # Save the image
                        image_name = f"dog{time.strftime('%Y-%m-%d_%H-%M-%S')}.jpg"
                        image_path = os.path.join(subfolder_path, image_name)
                        # Put text on image
                        text = f"{classNames[cls]}: {confidence:.2f}"  # Display class and confidence
                        cv2.putText(img, text, (x1, y1 - 10), font, fontScale, color, thickness)
                        # Put box on image
                        cv2.rectangle(img, (x1, y1), (x2, y2), color, 3)  # Change box color to green
                        cv2.imwrite(image_path, img)
        cap.release()
    except Exception as e:
        logging.error(f"An error occurred while capturing images: {e}")

def create_folder():
    try:
        # Create a folder for storing images
        current_directory = os.getcwd()
        images_folder = os.path.join(current_directory, "images")

        # Generate a unique subfolder name based on current timestamp
        subfolder_name = time.strftime("%Y-%m-%d_%H-%M-%S")
        subfolder_path = os.path.join(images_folder, subfolder_name)

        # Create the subfolder
        os.makedirs(subfolder_path)
        
        return subfolder_path
    
    except Exception as e:
        logging.error(f"An error occurred while creating folder: {e}")
        return None
    
if __name__ == "__main__":
    try:
        video_path = "./video/dog7.mp4"  # Path to your MP4 video file
        if not os.path.isfile(video_path):
            logging.error(f"Video file does not exist: {video_path}")
        else:
            subfolder_path = create_folder()
            if subfolder_path:
                # Load model
                model = YOLO("./best.pt")

                # Capture images when simulated sensor event occurs
                capture_duration = 60  # Duration to capture images (in seconds)

                # Simulate sensor event
                logging.info("Motion detection started.")
                logging.info("Starting image capture...")
                logging.info("Object Detection with TPU Accelerator...")
                capture_images(capture_duration, subfolder_path, classNames, video_path)

                cv2.destroyAllWindows()
            else:
                logging.error("Failed to create folder for storing images.")
    except Exception as e:
        logging.error(f"An unexpected error occurred: {e}")
