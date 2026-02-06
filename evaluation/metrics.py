import numpy as np

def attention_score(metrics):
    """
    Computes attention score using:
    - Blink count
    - Gaze magnitude stability
    - Pupil stability
    """

    # ---------------- BLINK PENALTY ----------------
    blink_penalty = metrics["blinks"] * 0.01

    # ---------------- GAZE STABILITY ----------------
    if metrics["gaze"]:
        gaze_magnitudes = [
            g["magnitude"] for g in metrics["gaze"]
            if isinstance(g, dict) and "magnitude" in g
        ]
        gaze_focus = 1 - np.mean(gaze_magnitudes) if gaze_magnitudes else 0.5
    else:
        gaze_focus = 0.5

    # ---------------- PUPIL STABILITY ----------------
    if metrics["pupil"]:
        pupil_stability = np.std(metrics["pupil"])
    else:
        pupil_stability = 0.5

    # ---------------- FINAL SCORE ----------------
    score = (
        gaze_focus * 0.4 +
        (1 - blink_penalty) * 0.3 +
        (1 - pupil_stability) * 0.3
    )

    return max(0.0, min(1.0, score))
