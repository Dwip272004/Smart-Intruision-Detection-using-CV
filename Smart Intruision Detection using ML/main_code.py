import cv2
import numpy as np
import os
from datetime import datetime
from ultralytics import YOLO
from telegram_alert import send_intrusion_alert

model = YOLO("yolov8n.pt")

if not os.path.exists("intrusions"):
    os.makedirs("intrusions")

cap = cv2.VideoCapture(0)
cv2.namedWindow("Frame")

roi_selected = False
roi = None
last_save_time = None

def is_intrusion(person_box, roi_box):
    px1, py1, px2, py2 = person_box
    rx, ry, rw, rh = roi_box
    rx2, ry2 = rx + rw, ry + rh
    ix1, iy1 = max(px1, rx), max(py1, ry)
    ix2, iy2 = min(px2, rx2), min(py2, ry2)
    return not (ix2 < ix1 or iy2 < iy1)

print("Press 's' to select ROI, 'q' to quit.")

while True:
    ret, frame = cap.read()
    if not ret:
        break

    if roi_selected:
        x, y, w, h = roi
        cv2.rectangle(frame, (x, y), (x+w, y+h), (0, 255, 0), 2)

        results = model(frame, verbose=False)
        intrusion_detected = False

        for result in results:
            for box in result.boxes:
                if int(box.cls) == 0:
                    x1, y1, x2, y2 = map(int, box.xyxy[0])
                    cv2.rectangle(frame, (x1, y1), (x2, y2), (0,50,255), 2)

                    if is_intrusion((x1, y1, x2, y2), roi):
                        intrusion_detected = True

        if intrusion_detected:
            cv2.putText(frame, "INTRUSION DETECTED!", (50, 50),
                        cv2.FONT_HERSHEY_SIMPLEX, 1.2, (0, 0, 255), 3)

            timestamp = datetime.now().strftime("%Y-%m-%d_%H-%M-%S")
            filename = f"intrusions/intrusion_{timestamp}.jpg"

            if not last_save_time or (datetime.now() - last_save_time).seconds > 3:
                cv2.imwrite(filename, frame)
                last_save_time = datetime.now()
                send_intrusion_alert(filename)
                print(f"Intruder detected — Snapshot saved: {filename}")

    cv2.imshow("Frame", frame)
    key = cv2.waitKey(30) & 0xFF

    if key == ord('s') and not roi_selected:
        roi = cv2.selectROI("Frame", frame, showCrosshair=True, fromCenter=False)
        roi_selected = True

    elif key == ord('q'):
        break

cap.release()
cv2.destroyAllWindows()
