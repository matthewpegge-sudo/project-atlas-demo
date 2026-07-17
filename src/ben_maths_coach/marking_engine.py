"""
Marking Engine — deterministic answer checks for prototype questions.

This module keeps marking separate from UI, LearnerDNA updates, rewards, and
persistence. It is intentionally simple for now.
"""

from __future__ import annotations

from decimal import Decimal, InvalidOperation
from fractions import Fraction

from ben_maths_coach.question_model import Question


def normalise_answer(text: str) -> str:
    """
    Prepare an answer for comparison.

    Handles simple algebra forms so these are treated the same: "4", "x=4",
    "x = 4", and "X = 4". Numeric equivalence is handled separately by
    `answers_match`.
    """
    answer = text.strip().lower()
    answer = "".join(answer.split())

    if answer.startswith("x="):
        return answer[2:]

    return answer


def _strip_percentage(answer: str, question: Question) -> str:
    """Remove a trailing percent sign only when a percentage answer is expected."""
    if not answer.endswith("%"):
        return answer

    question_text = question.question_text.lower()
    correct_answer = question.correct_answer.lower()
    expects_percentage = (
        correct_answer.endswith("%")
        or "percentage" in question_text
        or "percent" in question_text
    )
    if expects_percentage:
        return answer[:-1]
    return answer


def _as_number(answer: str) -> Fraction | None:
    """Convert simple numeric answers to Fractions for exact comparison."""
    if not answer:
        return None

    try:
        if "/" in answer:
            numerator, denominator = answer.split("/", maxsplit=1)
            if not numerator or not denominator:
                return None
            return Fraction(Decimal(numerator)) / Fraction(Decimal(denominator))
        return Fraction(Decimal(answer))
    except (InvalidOperation, TypeError, ValueError, ZeroDivisionError):
        return None


def answers_match(question: Question, learner_answer: str) -> bool:
    """Return whether a learner answer matches the question answer."""
    expected = normalise_answer(question.correct_answer)
    given = normalise_answer(learner_answer)

    expected = _strip_percentage(expected, question)
    given = _strip_percentage(given, question)

    if expected == given:
        return True

    expected_number = _as_number(expected)
    given_number = _as_number(given)
    if expected_number is None or given_number is None:
        return False

    return expected_number == given_number


def mark_answer(question: Question, learner_answer: str) -> tuple[bool, float, str]:
    """
    Mark using deterministic checks after normalisation.

    Returns (is_correct, marks_awarded, mistake_type). A full marking engine
    would handle partial marks, units, equivalent algebraic forms, and method
    marks later.
    """
    is_correct = answers_match(question, learner_answer)
    marks_awarded = float(question.marks_available) if is_correct else 0.0
    mistake_type = "" if is_correct else "incorrect_answer"
    return is_correct, marks_awarded, mistake_type
