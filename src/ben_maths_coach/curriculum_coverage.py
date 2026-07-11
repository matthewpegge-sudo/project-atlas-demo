"""
Curriculum Coverage — map the topic catalogue to available question content.

This module does not decide what Ben should do next and does not mark answers.
It only reports which curriculum topics currently have local questions.
"""

from __future__ import annotations

from collections import Counter
from dataclasses import dataclass
from typing import Sequence

from ben_maths_coach.question_bank import QUESTION_BANK
from ben_maths_coach.question_model import Question
from ben_maths_coach.topic_catalogue import Topic, TopicCatalogue


@dataclass(frozen=True)
class TopicCoverage:
    """Question coverage for one curriculum topic."""

    topic_id: str
    topic_name: str
    strand: str
    question_count: int

    @property
    def has_questions(self) -> bool:
        """Whether this topic currently has at least one local question."""
        return self.question_count > 0


def question_counts_by_topic(
    questions: Sequence[Question] = QUESTION_BANK,
) -> dict[str, int]:
    """Return the number of available questions for each topic id."""
    return dict(Counter(question.topic_id for question in questions))


def covered_topic_ids(questions: Sequence[Question] = QUESTION_BANK) -> set[str]:
    """Return topic ids that currently have at least one question."""
    return set(question_counts_by_topic(questions))


def has_questions_for_topic(
    topic_id: str,
    questions: Sequence[Question] = QUESTION_BANK,
) -> bool:
    """Return whether the local bank has questions for a topic."""
    return topic_id in covered_topic_ids(questions)


def coverage_for_catalogue(
    catalogue: TopicCatalogue,
    questions: Sequence[Question] = QUESTION_BANK,
) -> list[TopicCoverage]:
    """Return question coverage for every topic in catalogue order."""
    counts = question_counts_by_topic(questions)
    return [
        TopicCoverage(
            topic_id=topic.topic_id,
            topic_name=topic.name,
            strand=topic.strand,
            question_count=counts.get(topic.topic_id, 0),
        )
        for topic in catalogue.topics
    ]


def topics_with_question_coverage(
    catalogue: TopicCatalogue,
    questions: Sequence[Question] = QUESTION_BANK,
) -> tuple[Topic, ...]:
    """Return catalogue topics that currently have question coverage."""
    covered_ids = covered_topic_ids(questions)
    return tuple(topic for topic in catalogue.topics if topic.topic_id in covered_ids)
