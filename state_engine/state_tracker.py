import csv
from datetime import datetime
from backend.data_logger import get_user_dir


class ConversationState:
    def __init__(self, role_type):
        self.state = "INTRO"
        self.difficulty = 1
        self.confidence_score = 0.5
        self.role_type = role_type
        self.greeted = False

    def update(self, answer: str):
        # Simple confidence heuristic
        if len(answer.split()) > 20:
            self.confidence_score += 0.05

        if self.confidence_score > 0.7:
            self.difficulty += 1
            self.state = "DEEP_DIVE"

        # Role-based termination
        if self.role_type == "Intern" and self.difficulty >= 3:
            self.state = "WRAP_UP"

        if self.role_type == "Job" and self.difficulty >= 4:
            self.state = "WRAP_UP"


def log_session(state, question, answer, username):
    """
    Logs one Q/A turn for a specific user.
    """
    user_dir = get_user_dir(username)
    path = f"{user_dir}/session_logs.csv"

    with open(path, "a", newline="", encoding="utf-8") as f:
        writer = csv.writer(f)
        writer.writerow([
            datetime.now().isoformat(),
            state.state,
            state.difficulty,
            question,
            answer,
            round(state.confidence_score, 2)
        ])
