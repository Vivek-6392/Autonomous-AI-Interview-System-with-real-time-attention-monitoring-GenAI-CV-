import requests
from backend.config import *
from nemai.prompts import build_system_prompt, ROLE_FOCUS


class NemAIExaminer:
    def __init__(self, role_type, job_role, resume_text):
        self.role_type = role_type
        self.job_role = job_role
        self.focus = ROLE_FOCUS[job_role]

        self.system_prompt = build_system_prompt(
            role_type, job_role, resume_text
        )

        self.headers = {
            "Authorization": f"Bearer {OPENROUTER_API_KEY}",
            "Content-Type": "application/json"
        }

    def ask_question(self, state):
        """
        Asks exactly ONE question.
        Greeting is allowed ONLY on the first question.
        """

        messages = [
            {
                "role": "system",
                "content": self.system_prompt
            }
        ]

        # 🔒 Enforce greeting exactly once
        if state.greeted:
            messages.append({
                "role": "system",
                "content": (
                    "IMPORTANT: Do NOT greet the candidate. "
                    "Do NOT introduce yourself. "
                    "Ask ONLY the next technical question."
                )
            })

        messages.append({
            "role": "user",
            "content": (
                f"Interview phase: {state.state}\n"
                f"Difficulty level: {state.difficulty}\n"
                f"Primary focus areas: {self.focus}\n\n"
                f"Ask the NEXT technical question strictly aligned "
                f"with the role '{self.job_role}' and grounded "
                f"in the resume."
            )
        })

        payload = {
            "model": OPENROUTER_MODEL,
            "messages": messages
        }

        response = requests.post(
            OPENROUTER_URL,
            headers=self.headers,
            json=payload,
            timeout=30
        )

        response.raise_for_status()

        question = response.json()["choices"][0]["message"]["content"].strip()

        # 🔐 Lock greeting forever after first question
        if not state.greeted:
            state.greeted = True

        return question
