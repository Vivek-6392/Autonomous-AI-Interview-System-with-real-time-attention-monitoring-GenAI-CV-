import os
import pandas as pd
from backend.data_logger import get_user_dir
from evaluation.metrics import attention_score
from evaluation.scorer import grade


def generate_report(state, metrics, username):
    """
    Generate and persist final viva report exactly once.
    """
    user_dir = get_user_dir(username)

    attention = attention_score(metrics)
    cheating = metrics.get("multiple_face_frames", 0) > 15

    report = {
        "confidence_score": round(state.confidence_score, 2),
        "attention_score": round(attention, 2),
        "multiple_face_frames": metrics.get("multiple_face_frames", 0),
        "cheating_flag": cheating,
        "final_grade": "C" if cheating else grade(attention)
    }

    df = pd.DataFrame([report])
    df.to_csv(
        os.path.join(user_dir, "final_report.csv"),
        index=False
    )

    return report
