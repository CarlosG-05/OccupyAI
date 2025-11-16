import cv2
import numpy as np
import sys
import threading
import time
import requests
from ultralytics import YOLO
#import wifi

IMAGE_PATH = "test.jpg"

OUTPUT_IMAGE_PATH = "output.jpg"
CONFIDENCE_THRESHOLD = 0
SERVER_URL = "https://occupyai.onrender.com/update_occupancy"  # <-- Set your server URL here

ROOM_NUMBER = "LL-312"
FLOOR = 3
BUILDING = "Love Library"

def run_detection():
    print(f"Loading image from {IMAGE_PATH}...")
    frame = cv2.imread(IMAGE_PATH)
    if frame is None:
        print(f"Error: Failed to load image. Is the file '{IMAGE_PATH}' in the correct folder?")
        return

    print("Loading YOLOv8 model...")
    model = YOLO('yolov8n.pt')

    h, w, _ = frame.shape
    grid_rows, grid_cols = 2, 2  # 2x2 grid
    section_height = h // grid_rows
    section_width = w // grid_cols

    person_count = 0

    print("Running inference on each section...")
    for row in range(grid_rows):
        for col in range(grid_cols):
            y_start = row * section_height
            y_end = (row + 1) * section_height if row < grid_rows - 1 else h
            x_start = col * section_width
            x_end = (col + 1) * section_width if col < grid_cols - 1 else w
            section = frame[y_start:y_end, x_start:x_end]
            results = model(section)
            # Draw boxes and confidence on the section image
            section_person_count = 0
            for result in results:
                boxes = result.boxes
                for box in boxes:
                    cls = int(box.cls[0])
                    conf = float(box.conf[0])
                    if cls == 0 and conf > CONFIDENCE_THRESHOLD:
                        section_person_count += 1
                        x1, y1, x2, y2 = map(int, box.xyxy[0])
                        cv2.rectangle(section, (x1, y1), (x2, y2), (10, 255, 0), 2)
                        label = f'Person {section_person_count}: {int(conf * 100)}%'
                        cv2.putText(section, label, (x1, y1 - 10),
                                    cv2.FONT_HERSHEY_SIMPLEX, 0.5, (10, 255, 0), 2)
                        # Map box coordinates back to original image
                        person_count += 1
                        x1_full = x1 + x_start
                        x2_full = x2 + x_start
                        y1_full = y1 + y_start
                        y2_full = y2 + y_start
                        cv2.rectangle(frame, (x1_full, y1_full), (x2_full, y2_full), (10, 255, 0), 2)
                        label_full = f'Person {person_count}: {int(conf * 100)}%'
                        cv2.putText(frame, label_full, (x1_full, y1_full - 10),
                                    cv2.FONT_HERSHEY_SIMPLEX, 0.5, (10, 255, 0), 2)
            # Save the section image with boxes and labels
            section_filename = f'section_{row}_{col}.jpg'
            cv2.imwrite(section_filename, section)

    print(f"--- Detection Complete ---")
    print(f"Total People Detected: {person_count}")

    cv2.putText(frame, f'People Count: {person_count}', (30, 50),
                cv2.FONT_HERSHEY_SIMPLEX, 1, (255, 255, 0), 2, cv2.LINE_AA)
    cv2.imwrite(OUTPUT_IMAGE_PATH, frame)
    print(f"Success! Output image saved to: {OUTPUT_IMAGE_PATH}")

def run_camera():

    from picamera2 import Picamera2
    print("Loading YOLOv8 model...")
    model = YOLO('yolo11n_ncnn_model')
    picam2 = Picamera2()
    picam2.preview_configuration.main.size = (1280, 720)
    picam2.preview_configuration.main.format = "BGR888"
    picam2.preview_configuration.controls = {"FrameDurationLimits": (16667, 16667)}  # 60fps
    picam2.configure("preview")
    picam2.start()
    print("Starting live Picamera2 feed at 1280x720 60fps. Press 'q' to quit.")

    last_person_count = None

    def analyze_and_post(frame, person_count):
        payload = {
            "room_number": ROOM_NUMBER,
            "current_occupancy": person_count,
            "floor": FLOOR,
            "building": BUILDING
        }
        try:
            response = requests.post(SERVER_URL, json=payload)
            print("Posted:", payload, "Response:", response.status_code)
        except Exception as e:
            print("Error posting data:", e)
        print("Would post:", payload)

    while True:
        frame = picam2.capture_array()
        frame_bgr = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        results = model(frame_bgr)
        person_count = 0
        for result in results:
            boxes = result.boxes
            for box in boxes:
                cls = int(box.cls[0])
                conf = float(box.conf[0])
                if cls == 0 and conf > CONFIDENCE_THRESHOLD:
                    person_count += 1
                    x1, y1, x2, y2 = map(int, box.xyxy[0])
                    cv2.rectangle(frame_bgr, (x1, y1), (x2, y2), (10, 255, 0), 2)
                    label = f'Person {person_count}: {int(conf * 100)}%'
                    cv2.putText(frame_bgr, label, (x1, y1 - 10),
                                cv2.FONT_HERSHEY_SIMPLEX, 0.5, (10, 255, 0), 2)
        cv2.putText(frame_bgr, f'People Count: {person_count}', (30, 50),
                    cv2.FONT_HERSHEY_SIMPLEX, 1, (255, 255, 0), 2, cv2.LINE_AA)
        cv2.imshow('Live Picamera2 Feed', frame_bgr)
        # Only POST if person count changes
        if last_person_count is None or person_count != last_person_count:
            threading.Thread(target=analyze_and_post, args=(frame_bgr, person_count), daemon=True).start()
            last_person_count = person_count
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break
    cv2.destroyAllWindows()
    picam2.close()

if __name__ == '__main__':
    if len(sys.argv) > 2 and sys.argv[1] == 'source' and sys.argv[2] == 'camera':
        run_camera()
    else:
        run_detection()
