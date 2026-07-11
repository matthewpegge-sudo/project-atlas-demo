"""
Question Bank — small deterministic seed bank for demo missions.

This module deliberately stores local, hand-written questions only. It does
not choose recommendations, mark answers, call AI, or persist anything.
"""

from __future__ import annotations

from ben_maths_coach.learner_dna import ExamBoard
from ben_maths_coach.question_model import Question, SourceType


QUESTION_BANK: tuple[Question, ...] = (
    Question(
        question_id="linear-equations-001",
        topic_id="algebra.linear_equations",
        question_text="Solve: 2x + 5 = 13\nGive the value of x.",
        correct_answer="4",
        explanation=(
            "Subtract 5 from both sides: 2x = 8.\n"
            "Divide both sides by 2: x = 4."
        ),
        difficulty_grade=5,
        marks_available=2,
        source_type=SourceType.CUSTOM,
        exam_board=ExamBoard.AQA,
        calculator_allowed=False,
    ),
    Question(
        question_id="linear-equations-002",
        topic_id="algebra.linear_equations",
        question_text="Solve: 3x - 4 = 11\nGive the value of x.",
        correct_answer="5",
        explanation=(
            "Add 4 to both sides: 3x = 15.\n"
            "Divide both sides by 3: x = 5."
        ),
        difficulty_grade=5,
        marks_available=2,
        source_type=SourceType.CUSTOM,
        exam_board=ExamBoard.AQA,
        calculator_allowed=False,
    ),
    Question(
        question_id="linear-equations-003",
        topic_id="algebra.linear_equations",
        question_text="Solve: 5x + 2 = 22\nGive the value of x.",
        correct_answer="4",
        explanation=(
            "Subtract 2 from both sides: 5x = 20.\n"
            "Divide both sides by 5: x = 4."
        ),
        difficulty_grade=5,
        marks_available=2,
        source_type=SourceType.CUSTOM,
        exam_board=ExamBoard.AQA,
        calculator_allowed=False,
    ),
    Question(
        question_id="expressions-formulae-001",
        topic_id="algebra.expressions_and_formulae",
        question_text="Simplify: 3a + 2a\nGive your answer in its simplest form.",
        correct_answer="5a",
        explanation="3 lots of a plus 2 lots of a gives 5 lots of a, so the answer is 5a.",
        difficulty_grade=4,
        marks_available=1,
        source_type=SourceType.CUSTOM,
        exam_board=ExamBoard.AQA,
        calculator_allowed=False,
    ),
    Question(
        question_id="expressions-formulae-002",
        topic_id="algebra.expressions_and_formulae",
        question_text="Expand: 4(x + 3)\nGive your answer fully expanded.",
        correct_answer="4x+12",
        explanation="Multiply both terms inside the bracket by 4: 4 × x = 4x and 4 × 3 = 12.",
        difficulty_grade=4,
        marks_available=1,
        source_type=SourceType.CUSTOM,
        exam_board=ExamBoard.AQA,
        calculator_allowed=False,
    ),
    Question(
        question_id="expressions-formulae-003",
        topic_id="algebra.expressions_and_formulae",
        question_text="Factorise: 6x + 9\nGive your answer in factorised form.",
        correct_answer="3(2x+3)",
        explanation="The highest common factor of 6x and 9 is 3, so 6x + 9 = 3(2x + 3).",
        difficulty_grade=5,
        marks_available=2,
        source_type=SourceType.CUSTOM,
        exam_board=ExamBoard.AQA,
        calculator_allowed=False,
    ),
    Question(
        question_id="quadratics-001",
        topic_id="algebra.quadratics",
        question_text="Solve: x^2 = 49\nGive the positive value of x.",
        correct_answer="7",
        explanation="The square root of 49 is 7, so the positive value is x = 7.",
        difficulty_grade=5,
        marks_available=1,
        source_type=SourceType.CUSTOM,
        exam_board=ExamBoard.AQA,
        calculator_allowed=False,
    ),
    Question(
        question_id="quadratics-002",
        topic_id="algebra.quadratics",
        question_text="Solve: x^2 - 25 = 0\nGive the positive value of x.",
        correct_answer="5",
        explanation=(
            "Add 25 to both sides: x^2 = 25.\n"
            "The positive square root of 25 is 5."
        ),
        difficulty_grade=5,
        marks_available=2,
        source_type=SourceType.CUSTOM,
        exam_board=ExamBoard.AQA,
        calculator_allowed=False,
    ),
    Question(
        question_id="quadratics-003",
        topic_id="algebra.quadratics",
        question_text="Solve: x^2 + 6x + 9 = 0\nGive the value of x.",
        correct_answer="-3",
        explanation=(
            "Factorise x^2 + 6x + 9 as (x + 3)^2.\n"
            "So x + 3 = 0, which gives x = -3."
        ),
        difficulty_grade=6,
        marks_available=2,
        source_type=SourceType.CUSTOM,
        exam_board=ExamBoard.AQA,
        calculator_allowed=False,
    ),
    Question(
        question_id="simultaneous-equations-001",
        topic_id="algebra.simultaneous_equations",
        question_text=(
            "Solve the simultaneous equations:\n"
            "x + y = 10\n"
            "y = 6\n"
            "Give the value of x."
        ),
        correct_answer="4",
        explanation="Substitute y = 6 into x + y = 10. Then x + 6 = 10, so x = 4.",
        difficulty_grade=5,
        marks_available=2,
        source_type=SourceType.CUSTOM,
        exam_board=ExamBoard.AQA,
        calculator_allowed=False,
    ),
    Question(
        question_id="simultaneous-equations-002",
        topic_id="algebra.simultaneous_equations",
        question_text=(
            "Solve the simultaneous equations:\n"
            "x + y = 12\n"
            "x - y = 4\n"
            "Give the value of x."
        ),
        correct_answer="8",
        explanation="Add the equations to get 2x = 16. Divide by 2 to get x = 8.",
        difficulty_grade=6,
        marks_available=2,
        source_type=SourceType.CUSTOM,
        exam_board=ExamBoard.AQA,
        calculator_allowed=False,
    ),
    Question(
        question_id="simultaneous-equations-003",
        topic_id="algebra.simultaneous_equations",
        question_text=(
            "Solve the simultaneous equations:\n"
            "2x + y = 11\n"
            "y = 3\n"
            "Give the value of x."
        ),
        correct_answer="4",
        explanation="Substitute y = 3 into 2x + y = 11. Then 2x + 3 = 11, so x = 4.",
        difficulty_grade=6,
        marks_available=2,
        source_type=SourceType.CUSTOM,
        exam_board=ExamBoard.AQA,
        calculator_allowed=False,
    ),
    Question(
        question_id="percentage-change-001",
        topic_id="ratio.percentages",
        question_text="Increase 80 by 25%.\nGive the final value.",
        correct_answer="100",
        explanation="25% of 80 is 20. Add 20 to 80 to get 100.",
        difficulty_grade=4,
        marks_available=2,
        source_type=SourceType.CUSTOM,
        exam_board=ExamBoard.AQA,
        calculator_allowed=False,
    ),
    Question(
        question_id="percentage-change-002",
        topic_id="ratio.percentages",
        question_text="Decrease 60 by 10%.\nGive the final value.",
        correct_answer="54",
        explanation="10% of 60 is 6. Subtract 6 from 60 to get 54.",
        difficulty_grade=4,
        marks_available=2,
        source_type=SourceType.CUSTOM,
        exam_board=ExamBoard.AQA,
        calculator_allowed=False,
    ),
    Question(
        question_id="percentage-change-003",
        topic_id="ratio.percentages",
        question_text="A price rises from 40 to 50.\nWhat is the percentage increase?",
        correct_answer="25",
        explanation="The increase is 10. 10 out of 40 is 10 ÷ 40 = 0.25, which is 25%.",
        difficulty_grade=5,
        marks_available=2,
        source_type=SourceType.CUSTOM,
        exam_board=ExamBoard.AQA,
        calculator_allowed=False,
    ),
    Question(
        question_id="pythagoras-001",
        topic_id="geometry.pythagoras",
        question_text=(
            "A right-angled triangle has shorter sides 3 cm and 4 cm.\n"
            "Find the hypotenuse."
        ),
        correct_answer="5",
        explanation="Use a^2 + b^2 = c^2: 3^2 + 4^2 = 9 + 16 = 25, so c = 5.",
        difficulty_grade=5,
        marks_available=2,
        source_type=SourceType.CUSTOM,
        exam_board=ExamBoard.AQA,
        calculator_allowed=False,
    ),
    Question(
        question_id="pythagoras-002",
        topic_id="geometry.pythagoras",
        question_text=(
            "A right-angled triangle has shorter sides 5 cm and 12 cm.\n"
            "Find the hypotenuse."
        ),
        correct_answer="13",
        explanation=(
            "Use a^2 + b^2 = c^2: 5^2 + 12^2 = 25 + 144 = 169, so c = 13."
        ),
        difficulty_grade=5,
        marks_available=2,
        source_type=SourceType.CUSTOM,
        exam_board=ExamBoard.AQA,
        calculator_allowed=False,
    ),
    Question(
        question_id="pythagoras-003",
        topic_id="geometry.pythagoras",
        question_text=(
            "A right-angled triangle has hypotenuse 10 cm and one shorter side "
            "6 cm. Find the other shorter side."
        ),
        correct_answer="8",
        explanation="Use b^2 = c^2 - a^2: 10^2 - 6^2 = 100 - 36 = 64, so b = 8.",
        difficulty_grade=6,
        marks_available=2,
        source_type=SourceType.CUSTOM,
        exam_board=ExamBoard.AQA,
        calculator_allowed=False,
    ),
    Question(
        question_id="trigonometry-001",
        topic_id="geometry.trigonometry",
        question_text=(
            "In a right-angled triangle, the side opposite angle x is 6 cm "
            "and the hypotenuse is 10 cm.\n"
            "Find sin x."
        ),
        correct_answer="0.6",
        explanation="sin x = opposite ÷ hypotenuse = 6 ÷ 10 = 0.6.",
        difficulty_grade=5,
        marks_available=1,
        source_type=SourceType.CUSTOM,
        exam_board=ExamBoard.AQA,
        calculator_allowed=True,
    ),
    Question(
        question_id="trigonometry-002",
        topic_id="geometry.trigonometry",
        question_text=(
            "In a right-angled triangle, cos x = 0.5.\n"
            "x is acute. Find x in degrees."
        ),
        correct_answer="60",
        explanation="The acute angle with cosine 0.5 is 60 degrees.",
        difficulty_grade=6,
        marks_available=1,
        source_type=SourceType.CUSTOM,
        exam_board=ExamBoard.AQA,
        calculator_allowed=True,
    ),
    Question(
        question_id="trigonometry-003",
        topic_id="geometry.trigonometry",
        question_text=(
            "In a right-angled triangle, tan x = 1.\n"
            "x is acute. Find x in degrees."
        ),
        correct_answer="45",
        explanation="The acute angle with tangent 1 is 45 degrees.",
        difficulty_grade=6,
        marks_available=1,
        source_type=SourceType.CUSTOM,
        exam_board=ExamBoard.AQA,
        calculator_allowed=True,
    ),
)


def questions_for_topic(topic_id: str) -> list[Question]:
    """Return all questions for one topic in stable bank order."""
    return [question for question in QUESTION_BANK if question.topic_id == topic_id]


def select_mission_questions(topic_id: str, count: int = 3) -> list[Question]:
    """
    Return a deterministic mission question set for a topic.

    If the seed bank does not yet cover the requested topic, fall back to the
    first available questions so the prototype can still run.
    """
    if count <= 0:
        raise ValueError("Question count must be positive.")

    topic_questions = questions_for_topic(topic_id)
    if topic_questions:
        return topic_questions[:count]

    return list(QUESTION_BANK[:count])
