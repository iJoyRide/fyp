from ultralytics import YOLO
import cv2
import math
import os
from object_classes import classNames
import time

# Create a folder for storing images
current_directory = os.getcwd()
images_folder = os.path.join(current_directory, "images")

# Generate a unique subfolder name based on current timestamp
subfolder_name = time.strftime("%Y-%m-%d_%H-%M-%S")
subfolder_path = os.path.join(images_folder, subfolder_name)

# Create the subfolder
os.makedirs(subfolder_path)

# Start webcam
cap = cv2.VideoCapture(0)
cap.set(3, 640)
cap.set(4, 640)

# Model
model = YOLO("/models/yolov8n.pt")

# Initialize image counter
image_counter = 0

while True:
    success, img = cap.read()
    results = model(img, stream=True)

    # Coordinates
    for r in results:
        boxes = r.boxes

        for box in boxes:
            # Bounding box
            x1, y1, x2, y2 = box.xyxy[0]
            x1, y1, x2, y2 = int(x1), int(y1), int(x2), int(y2)  # convert to int values

            # Confidence
            confidence = math.ceil((box.conf[0] * 100)) / 100

            # Class name
            cls = int(box.cls[0])

            # Object details
            org = [x1, y1]
            font = cv2.FONT_HERSHEY_SIMPLEX
            fontScale = 1
            color = (255, 0, 0)
            thickness = 1

            if classNames[cls] == "dog":
                # Generate unique filename based on image_counter
                image_name = f"dog_{image_counter}.jpg"
                image_path = os.path.join(subfolder_path, image_name)

                # Check if file already exists
                while os.path.exists(image_path):
                    # If file exists, increment image_counter and generate new filename
                    image_counter += 1
                    image_name = f"dog_{image_counter}.jpg"
                    image_path = os.path.join(subfolder_path, image_name)

                # Put text on image
                cv2.putText(img, classNames[cls], org, font, fontScale, color, thickness)
                # Put box in cam
                cv2.rectangle(img, (x1, y1), (x2, y2), (255, 0, 255), 3)
                # Save the image
                cv2.imwrite(image_path, img)
                # Increment image_counter
                image_counter += 1

    cv2.imshow("Webcam", img)
    if cv2.waitKey(1) == ord("q"):
        break

cap.release()
cv2.destroyAllWindows()
