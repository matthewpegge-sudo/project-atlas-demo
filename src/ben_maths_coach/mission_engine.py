"""
Mission Engine — deterministic mission assembly and summary logic.

This module does not render UI, mark answers, update LearnerDNA, calculate
rewards, call AI, or persist anything. It prepares mission questions and turns
recorded attempts into a compact mission summary.
"""

from __future__ import annotations

from dataclasses import dataclass

from ben_maths_coach.question_bank import select_mission_questions
from ben_maths_coach.question_model import AnswerAttempt, Question
from ben_maths_coach.progress_engine import LearnerProgressSummary


@dataclass(frozen=True)
class MissionSummary:
    """A compact summary of one completed mission."""

    topic_id: str
    mastery_before: float
    mastery_after: float
    mistake_updated: bool
    questions_answered: int
    correct_answers: int
    average_confidence: int


def create_mission_questions(topic_id: str, count: int = 3) -> list[Question]:
    """Return the deterministic question set for a mission topic."""
    return select_mission_questions(topic_id, count=count)


def is_mission_complete(
    attempts: list[AnswerAttempt],
    questions: list[Question],
) -> bool:
    """Return True when every mission question has a recorded attempt."""
    return len(attempts) >= len(questions)


def summarize_mission(
    attempts: list[AnswerAttempt],
    learner_summaries: list[LearnerProgressSummary],
) -> MissionSummary:
    """Combine per-question attempts and learner updates into one mission summary."""
    if not attempts:
        raise ValueError("Cannot summarize a mission with no attempts.")
    if len(attempts) != len(learner_summaries):
        raise ValueError("Attempts and learner summaries must have the same length.")

    first_summary = learner_summaries[0]
    last_summary = learner_summaries[-1]

    return MissionSummary(
        topic_id=first_summary.topic_id,
        mastery_before=first_summary.old_mastery,
        mastery_after=last_summary.new_mastery,
        mistake_updated=any(summary.mistake_updated for summary in learner_summaries),
        questions_answered=len(attempts),
        correct_answers=sum(1 for attempt in attempts if attempt.is_correct),
        average_confidence=round(
            sum(attempt.confidence_before_answer for attempt in attempts)
            / len(attempts)
            * 100
        ),
    )
