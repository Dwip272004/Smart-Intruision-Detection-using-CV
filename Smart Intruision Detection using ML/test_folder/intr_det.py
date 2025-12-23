import cv2
import numpy as np
import os
from datetime import datetime

# Create folder for saved intrusions
if not os.path.exists("intrusions"):
    os.makedirs("intrusions")


cap = cv2.VideoCapture(0)
cv2.namedWindow("Frame")

roi_selected = False
roi = None
last_save_time = None

print("Press 's' to select ROI (bottle area), then 'q' to quit.")

while True:
    ret, frame = cap.read()
    if not ret:
        break

    if roi_selected:
        gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
        gray = cv2.GaussianBlur(gray, (21, 21), 0)

        # Extract ROI from current frame
        x, y, w, h = roi
        roi_curr = gray[y:y+h, x:x+w]

        # Compute difference
        diff = cv2.absdiff(reference_roi, roi_curr)
        _, thresh = cv2.threshold(diff, 25, 255, cv2.THRESH_BINARY)

        changed_area = np.sum(thresh) / 255

        # Draw rectangle
        color = (0, 255, 0)

        if changed_area > 200:  # adjust sensitivity
            color = (0, 0, 255)
            cv2.putText(frame, "INTRUSION DETECTED!", (50, 50),
                        cv2.FONT_HERSHEY_SIMPLEX, 1.2, (0, 0, 255), 3)
            print("Intrusion Detected!")

            # Save snapshot with timestamp
            timestamp = datetime.now().strftime("%Y-%m-%d_%H-%M-%S")
            filename = f"intrusions/intrusion_{timestamp}.jpg"

            # Save only if new intrusion or 5 seconds passed since last save
            if not last_save_time or (datetime.now() - last_save_time).seconds > 5:
                cv2.imwrite(filename, frame)
                last_save_time = datetime.now()
                print(f"Snapshot saved: {filename}")

        cv2.rectangle(frame, (x, y), (x+w, y+h), color, 2)
        cv2.imshow("Difference", thresh)

    cv2.imshow("Frame", frame)

    key = cv2.waitKey(30) & 0xFF

    if key == ord('s') and not roi_selected:
        roi = cv2.selectROI("Frame", frame, showCrosshair=True, fromCenter=False)
        x, y, w, h = roi
        roi_selected = True

        gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
        gray = cv2.GaussianBlur(gray, (21, 21), 0)
        reference_roi = gray[y:y+h, x:x+w]

        print("ROI selected. Monitoring started...")

    elif key == ord('q'):
        break

cap.release()
cv2.destroyAllWindows()
