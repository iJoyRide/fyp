import cv2
import math
import os
from ultralytics import YOLO
import time
import logging
from object_classes import classNames

# Configure logging
logging.basicConfig(level=logging.INFO)

# Function to capture images for a specific duration
def capture_images(duration, subfolder_path, classNames):
    try:
        start_time = time.time()
        while time.time() - start_time < duration:
            success, img = cap.read()
            if not success:
                logging.error("Failed to capture image from webcam.")
                continue
            
            results = model(img, stream=True)
            
            for r in results:
                boxes = r.boxes
                for box in boxes:
                    x1, y1, x2, y2 = map(int, box.xyxy[0])
                    cls = int(box.cls[0])
                    # Object details
                    org = [x1, y1]
                    font = cv2.FONT_HERSHEY_SIMPLEX
                    fontScale = 1
                    color = (255, 0, 0)
                    thickness = 1

                    if classNames[cls] == "cell phone":
                        # Save the image
                        image_name = f"cell phone{time.strftime('%Y-%m-%d_%H-%M-%S')}.jpg"
                        image_path = os.path.join(subfolder_path, image_name)
                        # Put text on image
                        cv2.putText(img, classNames[cls], (x1, y1), font, fontScale, color, thickness)
                        # Put box in cam
                        cv2.rectangle(img, (x1, y1), (x2, y2), (255, 0, 255), 3)
                        cv2.imwrite(image_path, img)
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
    cap = None
    try:
        # Initialize webcam
        cap = cv2.VideoCapture(0,cv2.CAP_DSHOW)
        cap.set(3, 640)
        cap.set(4, 640)
            
        subfolder_path = create_folder()
        if subfolder_path:
            # Model
            model = YOLO("/models/yolov8n.pt")

            # Capture images when simulated sensor event occurs
            capture_duration = 15  # Duration to capture images (in seconds)

            # Simulate sensor event
            logging.info("Starting image capture...")
            capture_images(capture_duration, subfolder_path, classNames)

            # Release webcam
            cap.release()
            cv2.destroyAllWindows()
        else:
            logging.error("Failed to create folder for storing images.")
    except Exception as e:
        logging.error(f"An unexpected error occurred: {e}")
