"""
Progress Engine — deterministic LearnerDNA updates from answer attempts.

This module owns the current prototype rules for mastery movement, confident
mistake recording, and session history updates. It does not render UI, choose
missions, mark answers, calculate rewards, call AI, or persist anything.
"""

from __future__ import annotations

from dataclasses import dataclass
from datetime import date, datetime

from ben_maths_coach.learner_dna import CommonMistake, LearnerDNA, SessionRecord
from ben_maths_coach.question_model import AnswerAttempt, Question


MASTERY_INCREASE = 0.05
MASTERY_DECREASE = 0.05
HIGH_CONFIDENCE_THRESHOLD = 0.7


@dataclass(frozen=True)
class LearnerProgressSummary:
    """What changed in LearnerDNA after one answer attempt."""

    topic_id: str
    old_mastery: float
    new_mastery: float
    old_confidence: float
    new_confidence: float
    mistake_updated: bool
    xp_earned: int
    total_xp: int


def clamp_score(value: float) -> float:
    """Keep a 0.0-1.0 score inside valid range."""
    return max(0.0, min(1.0, value))


def record_overconfident_mistake(learner: LearnerDNA, topic_id: str) -> bool:
    """
    Add or update a common mistake when the learner was confident but wrong.

    Returns True if a mistake record was created or updated.
    """
    description = "Incorrect answer despite high confidence"
    today = date.today()

    for mistake in learner.common_mistakes:
        if mistake.topic_id == topic_id and mistake.description == description:
            mistake.occurrence_count += 1
            mistake.last_seen = today
            return True

    learner.common_mistakes.append(
        CommonMistake(
            topic_id=topic_id,
            description=description,
            last_seen=today,
        )
    )
    return True


def update_learner_from_attempt(
    learner: LearnerDNA,
    question: Question,
    attempt: AnswerAttempt,
    session_started_at: datetime,
    xp_earned: int = 0,
) -> LearnerProgressSummary:
    """Update a learner profile after one answer attempt."""
    topic_id = question.topic_id
    old_mastery = learner.topic_mastery.get(topic_id, 0.0)
    old_confidence = learner.confidence_by_topic.get(topic_id, 0.0)
    new_confidence = clamp_score(attempt.confidence_before_answer)
    mistake_updated = False

    if attempt.is_correct:
        new_mastery = clamp_score(old_mastery + MASTERY_INCREASE)
    else:
        new_mastery = clamp_score(old_mastery - MASTERY_DECREASE)
        if attempt.confidence_before_answer >= HIGH_CONFIDENCE_THRESHOLD:
            mistake_updated = record_overconfident_mistake(learner, topic_id)

    learner.topic_mastery[topic_id] = new_mastery
    learner.confidence_by_topic[topic_id] = new_confidence
    learner.xp += xp_earned

    duration_minutes = max(1, round(attempt.time_taken_seconds / 60))
    learner.session_history.append(
        SessionRecord(
            started_at=session_started_at,
            duration_minutes=duration_minutes,
            topics_covered=[topic_id],
            xp_earned=xp_earned,
            notes=(
                f"Question {attempt.question_id}: "
                f"{'correct' if attempt.is_correct else 'incorrect'}"
            ),
        )
    )

    return LearnerProgressSummary(
        topic_id=topic_id,
        old_mastery=old_mastery,
        new_mastery=new_mastery,
        old_confidence=old_confidence,
        new_confidence=new_confidence,
        mistake_updated=mistake_updated,
        xp_earned=xp_earned,
        total_xp=learner.xp,
    )
