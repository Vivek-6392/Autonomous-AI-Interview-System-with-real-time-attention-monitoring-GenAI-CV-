import cv2

def detect_pupil(frame, landmarks):
    h, w, _ = frame.shape
    x = int(landmarks[468].x * w)
    y = int(landmarks[468].y * h)

    roi = frame[y-15:y+15, x-15:x+15]
    if roi.size == 0:
        return None

    gray = cv2.cvtColor(roi, cv2.COLOR_BGR2GRAY)
    _, thresh = cv2.threshold(gray, 50, 255, cv2.THRESH_BINARY_INV)
    cnts, _ = cv2.findContours(thresh, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)

    if cnts:
        (_, _), r = cv2.minEnclosingCircle(max(cnts, key=cv2.contourArea))
        return float(r)
    return None
