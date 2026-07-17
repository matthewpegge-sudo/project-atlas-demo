"""
Ben's Maths Coach — application entry point.

Run this file to start the app:

    python app.py

Or run the Streamlit mission screen:

    streamlit run app.py

Everything stays in memory — nothing is saved to disk or a database yet.
"""

from __future__ import annotations

import sys
import time
from datetime import datetime, timezone
from pathlib import Path

# Lets us import from src/ when running: python app.py
sys.path.insert(0, str(Path(__file__).resolve().parent / "src"))

from ben_maths_coach.decision_engine import (
    DecisionContext,
    LearningRecommendation,
    recommend_next_activity,
)
from ben_maths_coach.curriculum_coverage import (
    coverage_for_catalogue,
    has_questions_for_topic,
    topics_with_question_coverage,
)
from ben_maths_coach.learner_dna import (
    ExamBoard,
    LearnerDNA,
    PersonalDetails,
)
from ben_maths_coach.marking_engine import mark_answer
from ben_maths_coach.mission_engine import (
    MissionSummary,
    create_mission_questions,
    is_mission_complete,
    summarize_mission,
)
from ben_maths_coach.question_model import AnswerAttempt, Question, SourceType
from ben_maths_coach.progress_engine import (
    LearnerProgressSummary,
    update_learner_from_attempt,
)
from ben_maths_coach.rewards_engine import (
    AtlasWallet,
    MissionOutcome,
    RewardEngine,
    RewardSummary,
)
from ben_maths_coach.session_review import build_session_review
from ben_maths_coach.topic_catalogue import HIGHER_MATHS_CATALOGUE, TopicCatalogue


def running_in_streamlit() -> bool:
    """Return True when this file is being executed by Streamlit."""
    try:
        from streamlit.runtime.scriptrunner import get_script_run_ctx
    except ModuleNotFoundError:
        return False

    return get_script_run_ctx() is not None


def create_demo_learner() -> LearnerDNA:
    """Return a sample LearnerDNA profile for Ben with a few topic scores."""
    learner = LearnerDNA(
        personal_details=PersonalDetails(name="Ben", school="Example High"),
        exam_board=ExamBoard.AQA,
        target_grade=8,
        current_predicted_grade=6,
    )

    # Give every topic a baseline score so only the adjusted topics stand out.
    for topic_id in HIGHER_MATHS_CATALOGUE.topic_ids():
        learner.topic_mastery[topic_id] = 0.60
        learner.retention_by_topic[topic_id] = 0.70

    # Sample scores — linear equations is Ben's weakest topic right now.
    learner.topic_mastery["algebra.linear_equations"] = 0.35
    learner.retention_by_topic["algebra.linear_equations"] = 0.65
    learner.topic_mastery["algebra.quadratics"] = 0.50
    learner.retention_by_topic["algebra.quadratics"] = 0.55
    learner.topic_mastery["geometry.pythagoras"] = 0.82
    learner.retention_by_topic["geometry.pythagoras"] = 0.88

    return learner


def print_recommendation(recommendation: LearningRecommendation) -> None:
    """Show the Decision Engine's suggestion in the terminal."""
    print("--- Recommendation ---")
    print(f"Activity: {recommendation.activity_type.value.title()}")
    print(f"Topic: {recommendation.topic_name}")
    print(f"Suggested time: {recommendation.estimated_duration_minutes} minutes")
    print(f"\n{recommendation.explanation}")
    print("\nWhy:")
    for reason in recommendation.supporting_reasons:
        print(f"  • {reason}")
    print(
        "\nNote: Streamlit missions now use the seed question bank. "
        "The terminal demo still asks one fixed question."
    )


def create_demo_question() -> Question:
    """Return one hard-coded GCSE Higher question for the demo."""
    return Question(
        question_id="demo-001",
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
    )


def ask_confidence() -> float:
    """Ask the learner for a confidence score between 0 and 1."""
    while True:
        raw = input("How confident are you? (0 = guess, 1 = certain): ")
        try:
            confidence = float(raw)
        except ValueError:
            print("Please enter a number, for example 0.5")
            continue
        if 0.0 <= confidence <= 1.0:
            return confidence
        print("Confidence must be between 0 and 1.")


def print_learner_dna_update(summary: LearnerProgressSummary) -> None:
    """Show what changed in the learner profile after the attempt."""
    old_pct = round(summary.old_mastery * 100)
    new_pct = round(summary.new_mastery * 100)

    print("\n--- Learner DNA update ---")
    print(f"Topic: {summary.topic_id}")
    print(f"Mastery: {old_pct}% → {new_pct}%")
    print(f"XP earned: {summary.xp_earned} (total XP: {summary.total_xp})")
    print("Session history: 1 new session recorded")

    if summary.mistake_updated:
        print("Common mistakes: overconfidence mistake recorded or updated")
    else:
        print("Common mistakes: no change")


def print_next_recommendation(recommendation: LearningRecommendation) -> None:
    """Show what the Decision Engine suggests after the profile update."""
    print("\n--- Next recommendation ---")
    print(f"Activity: {recommendation.activity_type.value.title()}")
    print(f"Topic: {recommendation.topic_name}")
    print(f"Reason: {recommendation.explanation}")


def apply_streamlit_styles(st_module: object) -> None:
    """Apply simple responsive styling for the Streamlit app."""
    st = st_module
    st.markdown(
        """
        <style>
        :root {
            --atlas-text: #0f172a;
            --atlas-muted: #425466;
            --atlas-subtle: #64748b;
            --atlas-accent: #1d4ed8;
        }
        @media (prefers-color-scheme: dark) {
            :root {
                --atlas-text: #f8fafc;
                --atlas-muted: #cbd5e1;
                --atlas-subtle: #94a3b8;
                --atlas-accent: #93c5fd;
            }
        }
        .main .block-container {
            max-width: 760px;
            padding-top: 2rem;
            padding-bottom: 2rem;
        }
        .atlas-kicker {
            color: var(--atlas-muted);
            font-size: 0.9rem;
            font-weight: 700;
            letter-spacing: 0.04em;
            margin-bottom: 0.25rem;
        }
        .atlas-title {
            color: var(--atlas-text);
            font-size: 2.5rem;
            font-weight: 800;
            line-height: 1.05;
            margin: 0;
        }
        .coach-name {
            color: var(--atlas-accent);
            font-size: 1.25rem;
            font-weight: 700;
            margin-top: 0.5rem;
        }
        .mission-label {
            color: var(--atlas-subtle);
            font-size: 0.85rem;
            font-weight: 700;
            margin-bottom: 0.25rem;
            text-transform: uppercase;
        }
        .mission-value {
            color: var(--atlas-text);
            font-size: 1.1rem;
            font-weight: 700;
            margin-bottom: 1rem;
        }
        div.stButton > button {
            width: 100%;
            min-height: 3.25rem;
            border-radius: 8px;
            font-size: 1.05rem;
            font-weight: 800;
        }
        @media (max-width: 640px) {
            .main .block-container {
                padding-left: 1rem;
                padding-right: 1rem;
            }
            .atlas-title {
                font-size: 2rem;
            }
        }
        </style>
        """,
        unsafe_allow_html=True,
    )


def initialise_streamlit_state(st_module: object) -> None:
    """Set up in-memory Streamlit state for the demo session."""
    st = st_module
    if "learner" not in st.session_state:
        st.session_state.learner = create_demo_learner()
    if "wallet" not in st.session_state:
        st.session_state.wallet = AtlasWallet()
    if "screen" not in st.session_state:
        st.session_state.screen = "mission"
    if "session_started_at" not in st.session_state:
        st.session_state.session_started_at = None
    if "attempt_started_at" not in st.session_state:
        st.session_state.attempt_started_at = None
    if "mission_topic_id" not in st.session_state:
        st.session_state.mission_topic_id = None
    if "mission_questions" not in st.session_state:
        st.session_state.mission_questions = []
    if "current_question_index" not in st.session_state:
        st.session_state.current_question_index = 0
    if "mission_attempts" not in st.session_state:
        st.session_state.mission_attempts = []
    if "mission_summaries" not in st.session_state:
        st.session_state.mission_summaries = []
    if "session_result" not in st.session_state:
        st.session_state.session_result = None


def create_mission_outcome(summary: MissionSummary) -> MissionOutcome:
    """Build the rewards-engine input from an updated learner summary."""
    return MissionOutcome(
        mission_completed=True,
        mastery_before=summary.mastery_before,
        mastery_after=summary.mastery_after,
        recovery_applies=False,
        momentum_bonus_applies=False,
        breakthrough_applies=False,
    )


def apply_rewards_from_summary(
    learner: LearnerDNA,
    wallet: AtlasWallet,
    summary: MissionSummary,
) -> tuple[AtlasWallet, RewardSummary]:
    """Apply reward-engine results after a mission updates the learner."""
    reward_engine = RewardEngine()
    outcome = create_mission_outcome(summary)
    reward_summary = reward_engine.calculate_rewards(outcome)
    updated_wallet = reward_engine.apply_rewards(wallet, reward_summary)

    learner.xp = updated_wallet.xp
    if learner.session_history:
        learner.session_history[-1].xp_earned = reward_summary.total_xp

    return updated_wallet, reward_summary


def cash_equivalent_pounds(coins: int) -> float:
    """Return cash equivalent using 100 Atlas Coins = £1."""
    return coins / 100


def create_runnable_mission_catalogue() -> TopicCatalogue:
    """Return the subset of the curriculum that has local question content."""
    covered_topics = topics_with_question_coverage(HIGHER_MATHS_CATALOGUE)
    if not covered_topics:
        return HIGHER_MATHS_CATALOGUE

    return TopicCatalogue(
        name=f"{HIGHER_MATHS_CATALOGUE.name} - Seed Question Coverage",
        tier=HIGHER_MATHS_CATALOGUE.tier,
        topics=covered_topics,
    )


def curriculum_coverage_label() -> str:
    """Return a short label describing current question coverage."""
    coverage = coverage_for_catalogue(HIGHER_MATHS_CATALOGUE)
    covered_count = sum(item.has_questions for item in coverage)
    return (
        f"Seed question coverage: {covered_count} of {len(coverage)} "
        "GCSE Higher topics."
    )


def start_streamlit_session(st_module: object, topic_id: str) -> None:
    """Move from the mission screen into the demo question."""
    st = st_module
    now = datetime.now(timezone.utc)
    st.session_state.screen = "session"
    st.session_state.session_started_at = now
    st.session_state.attempt_started_at = time.monotonic()
    st.session_state.mission_topic_id = topic_id
    st.session_state.mission_questions = create_mission_questions(topic_id)
    st.session_state.current_question_index = 0
    st.session_state.mission_attempts = []
    st.session_state.mission_summaries = []
    st.session_state.session_result = None


def return_to_streamlit_mission(st_module: object) -> None:
    """Return to the mission screen."""
    st = st_module
    st.session_state.screen = "mission"
    st.session_state.session_result = None
    st.session_state.session_started_at = None
    st.session_state.attempt_started_at = None
    st.session_state.mission_topic_id = None
    st.session_state.mission_questions = []
    st.session_state.current_question_index = 0
    st.session_state.mission_attempts = []
    st.session_state.mission_summaries = []


def render_streamlit_header(st_module: object) -> None:
    """Render the shared app header."""
    st = st_module
    st.markdown(
        '<div class="atlas-kicker">Today&apos;s Mission</div>',
        unsafe_allow_html=True,
    )
    st.markdown('<h1 class="atlas-title">Project Atlas</h1>', unsafe_allow_html=True)
    st.markdown(
        '<div class="coach-name">Ben&rsquo;s Maths Coach</div>',
        unsafe_allow_html=True,
    )


def render_streamlit_mission(st_module: object) -> None:
    """Render the mission screen."""
    st = st_module
    learner = st.session_state.learner
    context = DecisionContext(available_minutes=25)
    mission_catalogue = create_runnable_mission_catalogue()
    recommendation = recommend_next_activity(
        learner,
        mission_catalogue,
        context,
    )
    recommended_topic_has_questions = has_questions_for_topic(recommendation.topic_id)

    render_streamlit_header(st)

    predicted_col, target_col = st.columns(2)
    predicted_col.metric("Predicted grade", learner.current_predicted_grade)
    target_col.metric("Target grade", learner.target_grade)

    with st.container(border=True):
        st.markdown(
            '<div class="mission-label">Recommended mission</div>',
            unsafe_allow_html=True,
        )
        st.markdown(
            f'<div class="mission-value">{recommendation.explanation}</div>',
            unsafe_allow_html=True,
        )

        detail_cols = st.columns(3)
        detail_cols[0].metric("Activity type", recommendation.activity_type.value.title())
        detail_cols[1].metric("Topic", recommendation.topic_name)
        detail_cols[2].metric(
            "Suggested minutes",
            recommendation.estimated_duration_minutes,
        )

        st.caption(curriculum_coverage_label())
        if recommended_topic_has_questions:
            st.caption("This recommended mission has local questions ready.")
        else:
            st.warning(
                "Atlas has identified this topic, but this prototype does not "
                "yet contain questions for it."
            )

        st.markdown(
            f"**Reason:** {recommendation.explanation}",
        )

    if st.button(
        "Start Session",
        type="primary",
        use_container_width=True,
        disabled=not recommended_topic_has_questions,
    ):
        start_streamlit_session(st, recommendation.topic_id)
        st.rerun()


def submit_streamlit_answer(
    st_module: object,
    question: Question,
    questions: list[Question],
    learner_answer: str,
    confidence_percent: int,
) -> None:
    """Mark one answer, update LearnerDNA, and finish the mission if needed."""
    st = st_module
    started_at = st.session_state.attempt_started_at or time.monotonic()
    session_started_at = st.session_state.session_started_at or datetime.now(
        timezone.utc
    )
    is_correct, marks_awarded, mistake_type = mark_answer(question, learner_answer)
    attempt = AnswerAttempt(
        question_id=question.question_id,
        learner_answer=learner_answer,
        is_correct=is_correct,
        marks_awarded=marks_awarded,
        time_taken_seconds=max(0, int(time.monotonic() - started_at)),
        confidence_before_answer=confidence_percent / 100,
        timestamp=datetime.now(timezone.utc),
        mistake_type=mistake_type,
    )

    summary = update_learner_from_attempt(
        st.session_state.learner,
        question,
        attempt,
        session_started_at,
    )

    st.session_state.mission_attempts.append(attempt)
    st.session_state.mission_summaries.append(summary)

    if not is_mission_complete(st.session_state.mission_attempts, questions):
        st.session_state.current_question_index += 1
        st.session_state.attempt_started_at = time.monotonic()
        return

    mission_summary = summarize_mission(
        st.session_state.mission_attempts,
        st.session_state.mission_summaries,
    )
    st.session_state.wallet, reward_summary = apply_rewards_from_summary(
        st.session_state.learner,
        st.session_state.wallet,
        mission_summary,
    )

    st.session_state.session_result = {
        "attempts": st.session_state.mission_attempts,
        "summaries": st.session_state.mission_summaries,
        "summary": mission_summary,
        "reward_summary": reward_summary,
        "wallet": st.session_state.wallet,
    }


def render_streamlit_result(st_module: object, questions: list[Question]) -> None:
    """Render the submitted answer result and mission completion summary."""
    st = st_module
    result = st.session_state.session_result
    attempts = result["attempts"]
    summary = result["summary"]
    reward_summary = result["reward_summary"]
    wallet = result["wallet"]
    old_mastery = round(summary.mastery_before * 100)
    new_mastery = round(summary.mastery_after * 100)
    topic = HIGHER_MATHS_CATALOGUE.get(summary.topic_id)
    topic_name = topic.name if topic is not None else summary.topic_id
    questions_answered = summary.questions_answered
    correct_answers = summary.correct_answers
    next_recommendation = recommend_next_activity(
        st.session_state.learner,
        create_runnable_mission_catalogue(),
        DecisionContext(available_minutes=25),
    )
    review = build_session_review(
        summary,
        attempts,
        next_recommendation.topic_name,
        next_recommendation.explanation,
    )

    if correct_answers == questions_answered:
        st.success("Mission complete — all correct")
    else:
        st.info("Mission complete")

    st.markdown("### Session review")

    with st.container(border=True):
        st.markdown(
            '<div class="mission-label">What you practised</div>',
            unsafe_allow_html=True,
        )
        st.markdown(f"**{topic_name}**")

        progress_cols = st.columns(3)
        progress_cols[0].metric(
            "Score",
            review.score_text,
        )
        progress_cols[1].metric(
            "Mastery",
            f"{new_mastery}%",
            f"{new_mastery - old_mastery}%",
        )
        progress_cols[2].metric(
            "Avg confidence",
            f"{summary.average_confidence}%",
        )

        answer_cols = st.columns(2)
        correct_text = (
            ", ".join(str(number) for number in review.correct_question_numbers)
            or "None yet"
        )
        missed_text = (
            ", ".join(str(number) for number in review.missed_question_numbers)
            or "None"
        )
        answer_cols[0].metric("Got right", correct_text)
        answer_cols[1].metric("Needs another look", missed_text)

        st.markdown(f"**Confidence vs accuracy:** {review.confidence_summary}")
        st.markdown(f"**What improved:** {review.what_went_well}")
        st.markdown(f"**What remains difficult:** {review.what_to_revisit}")
        st.markdown(f"**What Atlas learned:** {review.atlas_learned}")

    st.markdown("**Question review:**")
    for index, (question, attempt) in enumerate(zip(questions, attempts), start=1):
        with st.expander(
            f"Question {index}: {'Correct' if attempt.is_correct else 'Incorrect'}"
        ):
            st.markdown(f"**Question:** {question.question_text}")
            st.markdown(f"**Your answer:** {attempt.learner_answer or 'No answer'}")
            st.markdown(f"**Explanation:** {question.explanation}")

    result_cols = st.columns(3)
    result_cols[0].metric("XP earned", reward_summary.total_xp)
    result_cols[1].metric("Coins earned", reward_summary.total_coins)
    result_cols[2].metric(
        "Updated mastery",
        f"{new_mastery}%",
        f"{new_mastery - old_mastery}%",
    )

    st.markdown("**Rewards earned:**")
    for event in reward_summary.events:
        st.markdown(f"- {event.reason}")

    wallet_cols = st.columns(3)
    wallet_cols[0].metric("Wallet coins", wallet.coins)
    wallet_cols[1].metric(
        "Cash equivalent",
        f"£{cash_equivalent_pounds(wallet.coins):.2f}",
    )
    wallet_cols[2].metric("Lifetime coins", wallet.lifetime_coins)

    with st.container(border=True):
        st.markdown(
            '<div class="mission-label">What Atlas will do next</div>',
            unsafe_allow_html=True,
        )
        st.markdown(f"**{next_recommendation.topic_name}**")
        st.markdown(review.next_mission)

    if st.button("Return to Mission", use_container_width=True):
        return_to_streamlit_mission(st)
        st.rerun()


def render_streamlit_session(st_module: object) -> None:
    """Render the demo question and answer form."""
    st = st_module
    questions = st.session_state.mission_questions
    if not questions:
        questions = create_mission_questions("algebra.linear_equations")
        st.session_state.mission_questions = questions
    question_index = st.session_state.current_question_index
    question = questions[question_index]

    render_streamlit_header(st)

    with st.container(border=True):
        st.markdown(
            (
                f'<div class="mission-label">Question {question_index + 1} '
                f"of {len(questions)}</div>"
            ),
            unsafe_allow_html=True,
        )
        st.progress((question_index + 1) / len(questions))
        st.markdown(f"**{question.question_text}**")
        st.caption(f"{question.marks_available} marks")

        if st.session_state.session_result is None:
            with st.form(f"answer_form_{question.question_id}"):
                learner_answer = st.text_input("Your answer")
                confidence_percent = st.slider(
                    "Confidence",
                    min_value=0,
                    max_value=100,
                    value=50,
                    step=5,
                    format="%d%%",
                )
                submitted = st.form_submit_button(
                    "Submit",
                    type="primary",
                    use_container_width=True,
                )

            if submitted:
                submit_streamlit_answer(
                    st,
                    question,
                    questions,
                    learner_answer,
                    confidence_percent,
                )
                st.rerun()
        else:
            render_streamlit_result(st, questions)


def run_streamlit_app() -> None:
    """Render the Project Atlas Streamlit app."""
    import streamlit as st

    st.set_page_config(
        page_title="Project Atlas",
        layout="centered",
        initial_sidebar_state="collapsed",
    )

    apply_streamlit_styles(st)
    initialise_streamlit_state(st)

    if st.session_state.screen == "session":
        render_streamlit_session(st)
    else:
        render_streamlit_mission(st)


def run_demo_session(learner: LearnerDNA) -> AnswerAttempt:
    """Show a recommendation, then one question, mark it, and return an AnswerAttempt."""
    context = DecisionContext(available_minutes=25)
    recommendation = recommend_next_activity(
        learner,
        HIGHER_MATHS_CATALOGUE,
        context,
    )
    print_recommendation(recommendation)

    question = create_demo_question()

    print("\n--- Question ---")
    print(question.question_text)
    print(f"({question.marks_available} marks)\n")

    session_started_at = datetime.now(timezone.utc)
    started_at = time.monotonic()
    learner_answer = input("Your answer: ")
    confidence = ask_confidence()
    time_taken_seconds = int(time.monotonic() - started_at)

    is_correct, marks_awarded, mistake_type = mark_answer(question, learner_answer)

    attempt = AnswerAttempt(
        question_id=question.question_id,
        learner_answer=learner_answer,
        is_correct=is_correct,
        marks_awarded=marks_awarded,
        time_taken_seconds=time_taken_seconds,
        confidence_before_answer=confidence,
        timestamp=datetime.now(timezone.utc),
        mistake_type=mistake_type,
    )

    print("\n--- Result ---")
    if attempt.is_correct:
        print("Correct!")
    else:
        print("Not quite.")
    print(f"Marks awarded: {attempt.marks_awarded} / {question.marks_available}")
    print(f"\nExplanation:\n{question.explanation}")
    if attempt.mistake_type:
        print(f"\nMistake type: {attempt.mistake_type}")

    summary = update_learner_from_attempt(
        learner, question, attempt, session_started_at
    )
    _, reward_summary = apply_rewards_from_summary(
        learner,
        AtlasWallet(xp=learner.xp),
        summary,
    )
    print_learner_dna_update(summary)
    print(f"Coins earned: {reward_summary.total_coins}")
    print("Reward reasons:")
    for event in reward_summary.events:
        print(f"  • {event.reason}")

    next_recommendation = recommend_next_activity(
        learner,
        HIGHER_MATHS_CATALOGUE,
        context,
    )
    print_next_recommendation(next_recommendation)

    return attempt


def main() -> None:
    """Start the application."""
    if running_in_streamlit():
        run_streamlit_app()
        return

    print("Welcome to Ben's Maths Coach!")
    print("Project Atlas — demo session\n")

    learner = create_demo_learner()
    run_demo_session(learner)
    print("\nSession complete. (Nothing was saved — in memory only.)")


if __name__ == "__main__":
    main()
