import csv
import os

BASE_DATA_DIR = "data/users"

def sanitize_username(username: str) -> str:
    return "".join(c for c in username.lower() if c.isalnum() or c == "_")

def get_user_dir(username: str) -> str:
    user = sanitize_username(username)
    user_dir = os.path.join(BASE_DATA_DIR, user)
    os.makedirs(user_dir, exist_ok=True)
    return user_dir

def init_user_csvs(username: str):
    user_dir = get_user_dir(username)

    session_log = os.path.join(user_dir, "session_logs.csv")
    attention_log = os.path.join(user_dir, "attention_metrics.csv")

    if not os.path.exists(session_log):
        with open(session_log, "w", newline="", encoding="utf-8") as f:
            csv.writer(f).writerow([
                "timestamp", "state", "difficulty",
                "question", "answer", "confidence"
            ])

    if not os.path.exists(attention_log):
        with open(attention_log, "w", newline="", encoding="utf-8") as f:
            csv.writer(f).writerow([
                "timestamp", "blink", "gaze", "pupil"
            ])
