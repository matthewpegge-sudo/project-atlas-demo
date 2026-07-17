"""
Session Review - deterministic post-mission feedback.

This module turns a completed mission into a learner-facing review. It does
not render UI, mark answers, update LearnerDNA, calculate rewards, call AI, or
persist anything.
"""

from __future__ import annotations

from dataclasses import dataclass
from typing import Sequence

from ben_maths_coach.mission_engine import MissionSummary
from ben_maths_coach.question_model import AnswerAttempt


@dataclass(frozen=True)
class SessionReview:
    """A compact review of one completed mission."""

    score_text: str
    accuracy_percent: int
    confidence_summary: str
    correct_question_numbers: tuple[int, ...]
    missed_question_numbers: tuple[int, ...]
    what_went_well: str
    what_to_revisit: str
    atlas_learned: str
    next_mission: str


def _question_numbers(
    attempts: Sequence[AnswerAttempt], is_correct: bool
) -> tuple[int, ...]:
    """Return 1-based question numbers matching the correctness flag."""
    return tuple(
        index
        for index, attempt in enumerate(attempts, start=1)
        if attempt.is_correct is is_correct
    )


def _confidence_summary(attempts: Sequence[AnswerAttempt]) -> str:
    """Summarise confidence compared with accuracy."""
    confident_misses = sum(
        1
        for attempt in attempts
        if not attempt.is_correct and attempt.confidence_before_answer >= 0.7
    )
    uncertain_successes = sum(
        1
        for attempt in attempts
        if attempt.is_correct and attempt.confidence_before_answer <= 0.4
    )

    if confident_misses:
        return (
            "Ben was confident on a missed answer, so checking steps matters "
            "as much as getting started."
        )
    if uncertain_successes:
        return (
            "Ben got at least one answer right while feeling unsure, which is "
            "a useful confidence-building signal."
        )
    return "Ben's confidence broadly matched his answers in this mission."


def build_session_review(
    summary: MissionSummary,
    attempts: Sequence[AnswerAttempt],
    next_topic_name: str,
    next_explanation: str,
) -> SessionReview:
    """Create a deterministic learner-facing review for a completed mission."""
    if not attempts:
        raise ValueError("Cannot review a mission with no attempts.")

    correct_numbers = _question_numbers(attempts, True)
    missed_numbers = _question_numbers(attempts, False)
    accuracy_percent = round(summary.correct_answers / summary.questions_answered * 100)
    mastery_delta = round((summary.mastery_after - summary.mastery_before) * 100)

    if summary.correct_answers == summary.questions_answered:
        what_went_well = (
            "Ben completed every question correctly and strengthened this skill."
        )
        what_to_revisit = (
            "No urgent gaps from this mission. Atlas can keep this topic warm "
            "while moving the challenge on."
        )
        atlas_learned = (
            "Atlas learned that this topic is improving and can be used as a "
            "base for slightly harder work."
        )
    elif summary.mistake_updated:
        what_went_well = (
            "Ben completed the mission and produced useful learning data, even "
            "where answers were missed."
        )
        what_to_revisit = (
            "Revisit the missed question steps, especially the places where "
            "Ben felt confident but the answer was not correct."
        )
        atlas_learned = (
            "Atlas recorded a confident mistake, so future missions should "
            "give this skill another careful pass."
        )
    else:
        what_went_well = (
            "Ben completed the mission and answered part of the set correctly."
        )
        what_to_revisit = (
            "Revisit the missed questions and practise the same skill again "
            "before making it harder."
        )
        atlas_learned = (
            "Atlas updated mastery and confidence, and will keep this weakness "
            "visible when choosing the next mission."
        )

    if mastery_delta > 0:
        what_went_well = f"{what_went_well} Mastery moved up by {mastery_delta}%."
    elif mastery_delta < 0:
        what_to_revisit = f"{what_to_revisit} Mastery dipped by {abs(mastery_delta)}%."

    return SessionReview(
        score_text=f"{summary.correct_answers} / {summary.questions_answered}",
        accuracy_percent=accuracy_percent,
        confidence_summary=_confidence_summary(attempts),
        correct_question_numbers=correct_numbers,
        missed_question_numbers=missed_numbers,
        what_went_well=what_went_well,
        what_to_revisit=what_to_revisit,
        atlas_learned=atlas_learned,
        next_mission=f"{next_topic_name}: {next_explanation}",
    )
