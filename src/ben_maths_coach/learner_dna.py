"""
LearnerDNA — data model for a student's learning profile.

This module defines *what we know about a learner*, not how the app uses it.
All scores use a 0.0–1.0 scale unless noted otherwise.
"""

from __future__ import annotations

from dataclasses import dataclass, field
from datetime import date, datetime
from enum import Enum


class ExamBoard(str, Enum):
    """UK GCSE exam boards."""

    AQA = "AQA"
    EDEXCEL = "Edexcel"
    OCR = "OCR"
    WJEC = "WJEC"
    OTHER = "Other"


class ExamTier(str, Enum):
    """GCSE qualification tier."""

    FOUNDATION = "Foundation"
    HIGHER = "Higher"


@dataclass
class PersonalDetails:
    """Basic identity and contact information."""

    name: str
    email: str | None = None
    date_of_birth: date | None = None
    school: str | None = None


@dataclass
class LearningPreferences:
    """How the learner prefers to study."""

    prefers_step_by_step: bool = True
    prefers_visual_aids: bool = False
    prefers_short_sessions: bool = False
    typical_session_minutes: int = 30
    notes: str = ""


@dataclass
class StudyAvailability:
    """How much time the learner can realistically commit."""

    minutes_per_week: int = 0
    preferred_days: list[str] = field(default_factory=list)


@dataclass
class MotivationProfile:
    """Self-reported or inferred motivation."""

    score: float = 0.5  # 0.0 = low, 1.0 = high
    goal_note: str = ""


@dataclass
class ExamTechnique:
    """
    Non-topic-specific exam skills.

    Separate from knowledge and procedural skill — measures *how* they
    perform under exam conditions.
    """

    showing_working: float = 0.0
    time_management: float = 0.0
    checking_answers: float = 0.0
    interpreting_questions: float = 0.0


@dataclass
class CommonMistake:
    """A recurring error pattern we have observed."""

    topic_id: str
    description: str
    occurrence_count: int = 1
    last_seen: date | None = None


@dataclass
class RevisionEntry:
    """A single revision activity (outside a coached session)."""

    topic_id: str
    revised_on: date
    duration_minutes: int
    notes: str = ""


@dataclass
class SessionRecord:
    """A coached study session with the platform."""

    started_at: datetime
    duration_minutes: int
    topics_covered: list[str] = field(default_factory=list)
    xp_earned: int = 0
    notes: str = ""


@dataclass
class Achievement:
    """A milestone the learner has unlocked."""

    achievement_id: str
    title: str
    earned_at: datetime
    description: str = ""


@dataclass
class LearnerDNA:
    """
    Complete learning profile for one student.

    Topic-keyed fields (mastery, confidence, etc.) use topic_id strings
    as keys, e.g. "algebra.quadratics". The topic catalogue itself is
    defined elsewhere — this model only stores per-learner values.
    """

    # Identity and exam context
    personal_details: PersonalDetails
    exam_board: ExamBoard
    target_grade: int  # GCSE grade 1–9
    current_predicted_grade: int  # GCSE grade 1–9
    tier: ExamTier = ExamTier.HIGHER

    # Per-topic learning state (keys = topic_id)
    topic_mastery: dict[str, float] = field(default_factory=dict)
    confidence_by_topic: dict[str, float] = field(default_factory=dict)
    knowledge_by_topic: dict[str, float] = field(default_factory=dict)
    skill_by_topic: dict[str, float] = field(default_factory=dict)
    retention_by_topic: dict[str, float] = field(default_factory=dict)

    # Observed patterns and preferences
    common_mistakes: list[CommonMistake] = field(default_factory=list)
    learning_preferences: LearningPreferences = field(
        default_factory=LearningPreferences
    )
    available_study_time: StudyAvailability = field(
        default_factory=StudyAvailability
    )

    # History
    revision_history: list[RevisionEntry] = field(default_factory=list)
    session_history: list[SessionRecord] = field(default_factory=list)

    # Gamification
    xp: int = 0
    level: int = 1
    achievements: list[Achievement] = field(default_factory=list)

    # Broader learning profile
    motivation: MotivationProfile = field(default_factory=MotivationProfile)
    exam_technique: ExamTechnique = field(default_factory=ExamTechnique)
