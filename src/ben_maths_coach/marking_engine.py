"""
Marking Engine — deterministic answer checks for prototype questions.

This module keeps marking separate from UI, LearnerDNA updates, rewards, and
persistence. It is intentionally simple for now.
"""

from __future__ import annotations

from ben_maths_coach.question_model import Question


def normalise_answer(text: str) -> str:
    """
    Prepare an answer for comparison.

    Handles simple algebra forms so these are treated the same: "4", "x=4",
    "x = 4", and "X = 4".
    """
    answer = text.strip().lower()
    answer = answer.replace(" ", "")

    if answer.startswith("x="):
        return answer[2:]

    return answer


def mark_answer(question: Question, learner_answer: str) -> tuple[bool, float, str]:
    """
    Mark using a simple answer check after normalisation.

    Returns (is_correct, marks_awarded, mistake_type). A full marking engine
    would handle partial marks, units, equivalent forms, and method marks later.
    """
    is_correct = normalise_answer(learner_answer) == normalise_answer(
        question.correct_answer
    )
    marks_awarded = float(question.marks_available) if is_correct else 0.0
    mistake_type = "" if is_correct else "incorrect_answer"
    return is_correct, marks_awarded, mistake_type
