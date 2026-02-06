import cv2
import csv
from datetime import datetime
import mediapipe as mp

from mediapipe.tasks import python
from mediapipe.tasks.python import vision
from backend.data_logger import get_user_dir

from vision.blink_detector import detect_blink
from vision.pupil_tracker import detect_pupil
from vision.gaze_estimator import estimate_gaze


class VisionPipeline:
    def __init__(self, username):
        self.username = username
        self.cap = cv2.VideoCapture(0)

        base_options = python.BaseOptions(
            model_asset_path="models/face_landmarker.task"
        )
        options = vision.FaceLandmarkerOptions(
            base_options=base_options,
            num_faces=5  # allow detection of multiple faces
        )

        self.landmarker = vision.FaceLandmarker.create_from_options(options)

        self.metrics = {
            "blinks": 0,
            "gaze": [],
            "pupil": [],
            "multiple_face_frames": 0
        }

    def process_frame(self):
        ret, frame = self.cap.read()
        if not ret:
            return None

        rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        mp_image = mp.Image(mp.ImageFormat.SRGB, rgb)
        result = self.landmarker.detect(mp_image)

        # -------- MULTI-FACE CHEATING DETECTION --------
        face_count = len(result.face_landmarks) if result.face_landmarks else 0

        if face_count > 1:
            self.metrics["multiple_face_frames"] += 1

        # -------- PROCESS PRIMARY FACE ONLY --------
        if face_count >= 1:
            landmarks = result.face_landmarks[0]

            blink = detect_blink(landmarks)
            gaze = estimate_gaze(landmarks)
            pupil = detect_pupil(frame, landmarks)

            self.metrics["blinks"] += blink
            self.metrics["gaze"].append(gaze)
            if pupil:
                self.metrics["pupil"].append(pupil)

            user_dir = get_user_dir(self.username)
            with open(
                f"{user_dir}/attention_metrics.csv",
                "a",
                newline="",
                encoding="utf-8"
            ) as f:
                csv.writer(f).writerow([
                    datetime.now().isoformat(),
                    blink,
                    gaze,
                    pupil,
                    face_count
                ])

        return frame

    def cheating_detected(self):
        # Threshold: more than 15 frames with multiple faces
        return self.metrics["multiple_face_frames"] > 15

    def release(self):
        self.cap.release()
        self.landmarker.close()
    
    def process_external_frame(self, frame):
        import cv2
        import csv
        from datetime import datetime
        import mediapipe as mp
        from backend.data_logger import get_user_dir

        rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        mp_image = mp.Image(mp.ImageFormat.SRGB, rgb)
        result = self.landmarker.detect(mp_image)

        face_count = len(result.face_landmarks) if result.face_landmarks else 0

        if face_count > 1:
            self.metrics["multiple_face_frames"] += 1

        blink = 0
        gaze = None
        pupil = None

        if face_count >= 1:
            landmarks = result.face_landmarks[0]
            blink = detect_blink(landmarks)
            gaze = estimate_gaze(landmarks)
            pupil = detect_pupil(frame, landmarks)

            self.metrics["blinks"] += blink
            self.metrics["gaze"].append(gaze)
            if pupil:
                self.metrics["pupil"].append(pupil)

        user_dir = get_user_dir(self.username)
        with open(
            f"{user_dir}/attention_metrics.csv",
            "a",
            newline="",
            encoding="utf-8"
        ) as f:
            csv.writer(f).writerow([
                datetime.now().isoformat(),
                blink,
                gaze["magnitude"] if isinstance(gaze, dict) else None,
                pupil,
                face_count
            ])

        return frame
