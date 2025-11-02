import cv2
import numpy as np
import sys
from ultralytics import YOLO

IMAGE_PATH = "test.jpg"
OUTPUT_IMAGE_PATH = "output.jpg"
CONFIDENCE_THRESHOLD = 0

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
    print("Loading YOLOv8 model...")
    model = YOLO('yolov8n.pt')
    cap = cv2.VideoCapture(0)
    if not cap.isOpened():
        print("Error: Could not open camera.")
        return
    print("Starting live camera feed. Press 'q' to quit.")
    while True:
        ret, frame = cap.read()
        if not ret:
            print("Failed to grab frame.")
            break
        results = model(frame)
        person_count = 0
        for result in results:
            boxes = result.boxes
            for box in boxes:
                cls = int(box.cls[0])
                conf = float(box.conf[0])
                if cls == 0 and conf > CONFIDENCE_THRESHOLD:
                    person_count += 1
                    x1, y1, x2, y2 = map(int, box.xyxy[0])
                    cv2.rectangle(frame, (x1, y1), (x2, y2), (10, 255, 0), 2)
                    label = f'Person {person_count}: {int(conf * 100)}%'
                    cv2.putText(frame, label, (x1, y1 - 10),
                                cv2.FONT_HERSHEY_SIMPLEX, 0.5, (10, 255, 0), 2)
        cv2.putText(frame, f'People Count: {person_count}', (30, 50),
                    cv2.FONT_HERSHEY_SIMPLEX, 1, (255, 255, 0), 2, cv2.LINE_AA)
        cv2.imshow('Live Feed', frame)
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break
    cap.release()
    cv2.destroyAllWindows()

if __name__ == '__main__':
    if len(sys.argv) > 2 and sys.argv[1] == 'source' and sys.argv[2] == 'camera':
        run_camera()
    else:
        run_detection()