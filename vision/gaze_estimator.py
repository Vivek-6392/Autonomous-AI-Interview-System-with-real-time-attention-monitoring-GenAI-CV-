import numpy as np

def estimate_gaze(landmarks):
    left = np.array([landmarks[33].x, landmarks[33].y])
    right = np.array([landmarks[133].x, landmarks[133].y])
    pupil = np.array([landmarks[468].x, landmarks[468].y])

    eye_center = (left + right) / 2
    gaze_vector = pupil - eye_center

    return {
        "magnitude": float(np.linalg.norm(gaze_vector)),
        "direction": gaze_vector.tolist()
    }
