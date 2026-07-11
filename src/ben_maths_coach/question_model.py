"""
Question model — questions and learner answer attempts.

Defines *what a question is* and *what we record when a learner answers*.
Marking logic lives elsewhere — this module is data only.
"""

from __future__ import annotations

from dataclasses import dataclass
from datetime import datetime
from enum import Enum

from ben_maths_coach.learner_dna import ExamBoard


class SourceType(str, Enum):
    """Where a question came from."""

    GENERATED = "generated"
    PAST_PAPER = "past_paper"
    CUSTOM = "custom"


@dataclass
class Question:
    """
    One GCSE Maths question.

    `topic_id` should match an id from the topic catalogue (e.g.
    "algebra.quadratics"). `difficulty_grade` is the GCSE grade band the
    question is aimed at, from 4 (easier Higher) to 9 (hardest).
    """

    question_id: str
    topic_id: str
    question_text: str
    correct_answer: str
    explanation: str
    difficulty_grade: int  # GCSE grade 4–9
    marks_available: int
    source_type: SourceType
    exam_board: ExamBoard | None = None
    paper_reference: str | None = None
    calculator_allowed: bool | None = None


@dataclass
class AnswerAttempt:
    """
    A single learner response to one question.

    Recorded after the learner submits an answer. `mistake_type` is a short
    label for the kind of error made (e.g. "sign_error") — empty when
    the answer is correct or not yet classified.
    """

    question_id: str
    learner_answer: str
    is_correct: bool
    marks_awarded: float
    time_taken_seconds: int
    confidence_before_answer: float  # 0.0 = not confident, 1.0 = very confident
    timestamp: datetime
    mistake_type: str = ""
