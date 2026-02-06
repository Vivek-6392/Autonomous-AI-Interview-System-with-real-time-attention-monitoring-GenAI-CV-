from scipy.spatial import distance as dist

LEFT_EYE = [33, 160, 158, 133, 153, 144]

def detect_blink(landmarks):
    eye = [(landmarks[i].x, landmarks[i].y) for i in LEFT_EYE]
    A = dist.euclidean(eye[1], eye[5])
    B = dist.euclidean(eye[2], eye[4])
    C = dist.euclidean(eye[0], eye[3])
    ear = (A + B) / (2 * C)
    return 1 if ear < 0.25 else 0
