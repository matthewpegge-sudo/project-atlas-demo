"""
Decision Engine — choose the single best next learning activity.

Given a learner profile and topic catalogue, returns one recommendation.
Scoring is intentionally simple for now; rules can grow later.
"""

from __future__ import annotations

from dataclasses import dataclass, field
from datetime import date
from enum import Enum

from ben_maths_coach.learner_dna import LearnerDNA
from ben_maths_coach.topic_catalogue import Topic, TopicCatalogue

MISTAKE_MEMORY_THRESHOLD = 2
MISTAKE_MEMORY_WEIGHT = 0.05
MAX_MISTAKE_MEMORY_WEIGHT = 0.20


class ActivityType(str, Enum):
    """Kind of learning activity to do next."""

    PRACTICE = "practice"
    REVIEW = "review"
    STRETCH = "stretch"


@dataclass
class DecisionContext:
    """Extra information for one recommendation request."""

    exam_date: date | None = None
    available_minutes: int | None = None


@dataclass
class LearningRecommendation:
    """One recommended next step for the learner."""

    activity_type: ActivityType
    topic_id: str
    topic_name: str
    estimated_duration_minutes: int
    explanation: str
    supporting_reasons: list[str] = field(default_factory=list)


def _mastery_for_topic(learner: LearnerDNA, topic_id: str) -> float:
    """Return mastery for a topic, or 0.0 if not recorded yet."""
    return learner.topic_mastery.get(topic_id, 0.0)


def _retention_for_topic(learner: LearnerDNA, topic_id: str) -> float:
    """Return retention for a topic, or 0.0 if not recorded yet."""
    return learner.retention_by_topic.get(topic_id, 0.0)


def _confidence_for_topic(learner: LearnerDNA, topic_id: str) -> float:
    """Return confidence for a topic, or 0.0 if not recorded yet."""
    return learner.confidence_by_topic.get(topic_id, 0.0)


def _recurring_mistakes_for_topic(learner: LearnerDNA, topic_id: str) -> int:
    """Return the total observed recurring mistake count for a topic."""
    return sum(
        mistake.occurrence_count
        for mistake in learner.common_mistakes
        if mistake.topic_id == topic_id
        and mistake.occurrence_count >= MISTAKE_MEMORY_THRESHOLD
    )


def _mistake_memory_pressure(learner: LearnerDNA, topic_id: str) -> float:
    """
    Convert recurring mistakes into a small deterministic priority boost.

    This lowers the topic's effective mastery for recommendation ranking only;
    it does not change LearnerDNA mastery itself.
    """
    mistake_count = _recurring_mistakes_for_topic(learner, topic_id)
    return min(
        mistake_count * MISTAKE_MEMORY_WEIGHT,
        MAX_MISTAKE_MEMORY_WEIGHT,
    )


def _choose_weakest_topic(learner: LearnerDNA, catalogue: TopicCatalogue) -> Topic:
    """
    Pick the topic with the lowest effective mastery score.

    Recurring mistakes gently lower effective mastery for selection, so Atlas
    can revisit topics where Ben is repeatedly getting tripped up. If two
    topics tie, lower confidence wins. If they also tie on confidence, the
    smaller topic_id wins so the result is deterministic.
    """
    return min(
        catalogue.topics,
        key=lambda topic: (
            _mastery_for_topic(learner, topic.topic_id)
            - _mistake_memory_pressure(learner, topic.topic_id),
            _confidence_for_topic(learner, topic.topic_id),
            topic.topic_id,
        ),
    )


def _choose_activity_type(mastery: float, retention: float) -> ActivityType:
    """Pick activity type from mastery and retention on the chosen topic."""
    if retention < 0.4:
        return ActivityType.REVIEW
    if mastery < 0.5:
        return ActivityType.PRACTICE
    return ActivityType.STRETCH


def _estimate_duration_minutes(
    learner: LearnerDNA, context: DecisionContext
) -> int:
    """Use session minutes from context, or fall back to learner preference."""
    if context.available_minutes is not None:
        return context.available_minutes
    return learner.learning_preferences.typical_session_minutes


def _build_explanation(
    topic: Topic,
    activity_type: ActivityType,
    mastery: float,
    retention: float,
    confidence: float,
    recurring_mistakes: int,
) -> tuple[str, list[str]]:
    """Return a main explanation and supporting reason bullets."""
    mastery_pct = round(mastery * 100)
    retention_pct = round(retention * 100)
    confidence_pct = round(confidence * 100)

    if activity_type is ActivityType.REVIEW:
        explanation = (
            f"Review {topic.name} — retention is {retention_pct}%, "
            f"so it is worth refreshing before you forget it."
        )
    elif activity_type is ActivityType.PRACTICE:
        explanation = (
            f"Practise {topic.name} — mastery is {mastery_pct}%, "
            f"so this topic needs more work."
        )
    else:
        explanation = (
            f"Stretch yourself on {topic.name} — mastery is {mastery_pct}% "
            f"and retention is {retention_pct}%, so you are ready for a challenge."
        )

    supporting_reasons = [
        f"Lowest mastery in the catalogue ({mastery_pct}%).",
        f"Retention on this topic: {retention_pct}%.",
        f"Confidence on this topic: {confidence_pct}%.",
        f"Activity chosen: {activity_type.value}.",
    ]
    if recurring_mistakes:
        supporting_reasons.insert(
            3,
            f"Recurring mistakes on this topic: {recurring_mistakes} observations.",
        )
    return explanation, supporting_reasons


def recommend_next_activity(
    learner: LearnerDNA,
    catalogue: TopicCatalogue,
    context: DecisionContext | None = None,
) -> LearningRecommendation:
    """
    Recommend the single best next learning activity.

    Simple rules for now:
    1. Choose the topic with the lowest effective mastery.
       Missing mastery counts as 0.0, and recurring mistakes add a small
       deterministic priority boost.
    2. If retention on that topic is below 0.4, recommend REVIEW.
    3. Else if mastery is below 0.5, recommend PRACTICE.
    4. Else recommend STRETCH.
    """
    if context is None:
        context = DecisionContext()

    if not catalogue.topics:
        raise ValueError("Topic catalogue is empty — cannot recommend an activity.")

    topic = _choose_weakest_topic(learner, catalogue)
    mastery = _mastery_for_topic(learner, topic.topic_id)
    retention = _retention_for_topic(learner, topic.topic_id)
    confidence = _confidence_for_topic(learner, topic.topic_id)
    recurring_mistakes = _recurring_mistakes_for_topic(learner, topic.topic_id)
    activity_type = _choose_activity_type(mastery, retention)
    explanation, supporting_reasons = _build_explanation(
        topic, activity_type, mastery, retention, confidence, recurring_mistakes
    )

    return LearningRecommendation(
        activity_type=activity_type,
        topic_id=topic.topic_id,
        topic_name=topic.name,
        estimated_duration_minutes=_estimate_duration_minutes(learner, context),
        explanation=explanation,
        supporting_reasons=supporting_reasons,
    )
