"""
Atlas Rewards — deterministic reward calculations.

This module is deliberately independent from Streamlit and persistence. It
turns a mission outcome into reward events, then applies those events to an
in-memory wallet.
"""

from __future__ import annotations

from dataclasses import dataclass
from enum import Enum


@dataclass(frozen=True)
class AtlasWallet:
    """Current reward balance for a learner."""

    xp: int = 0
    coins: int = 0
    lifetime_coins: int = 0
    momentum: int = 0


class RewardType(str, Enum):
    """Types of rewards Atlas can award."""

    MISSION_COMPLETE = "MISSION_COMPLETE"
    MASTERY_IMPROVEMENT = "MASTERY_IMPROVEMENT"
    RECOVERY_BONUS = "RECOVERY_BONUS"
    MOMENTUM_BONUS = "MOMENTUM_BONUS"
    BREAKTHROUGH = "BREAKTHROUGH"


@dataclass(frozen=True)
class RewardEvent:
    """One reward earned from a mission outcome."""

    reward_type: RewardType
    coins: int
    xp: int
    reason: str


@dataclass(frozen=True)
class MissionOutcome:
    """Signals from a completed learning mission."""

    mission_completed: bool
    mastery_before: float
    mastery_after: float
    recovery_applies: bool = False
    momentum_bonus_applies: bool = False
    breakthrough_applies: bool = False


@dataclass(frozen=True)
class RewardSummary:
    """All rewards earned from a mission outcome."""

    events: list[RewardEvent]
    total_coins: int
    total_xp: int


class RewardEngine:
    """Calculate and apply Atlas Rewards."""

    SIGNIFICANT_MASTERY_INCREASE = 0.10
    FLOAT_TOLERANCE = 0.000001

    def calculate_rewards(self, outcome: MissionOutcome) -> RewardSummary:
        """Return a reward summary for a mission outcome."""
        events: list[RewardEvent] = []

        if outcome.mission_completed:
            events.append(
                RewardEvent(
                    reward_type=RewardType.MISSION_COMPLETE,
                    coins=10,
                    xp=100,
                    reason="Mission completed.",
                )
            )

        if (
            outcome.mastery_after - outcome.mastery_before
            >= self.SIGNIFICANT_MASTERY_INCREASE - self.FLOAT_TOLERANCE
        ):
            events.append(
                RewardEvent(
                    reward_type=RewardType.MASTERY_IMPROVEMENT,
                    coins=5,
                    xp=0,
                    reason="Mastery improved significantly.",
                )
            )

        if outcome.recovery_applies:
            events.append(
                RewardEvent(
                    reward_type=RewardType.RECOVERY_BONUS,
                    coins=5,
                    xp=0,
                    reason="Recovery bonus earned.",
                )
            )

        if outcome.momentum_bonus_applies:
            events.append(
                RewardEvent(
                    reward_type=RewardType.MOMENTUM_BONUS,
                    coins=5,
                    xp=0,
                    reason="Momentum bonus earned.",
                )
            )

        if outcome.breakthrough_applies:
            events.append(
                RewardEvent(
                    reward_type=RewardType.BREAKTHROUGH,
                    coins=20,
                    xp=0,
                    reason="Breakthrough achieved.",
                )
            )

        return RewardSummary(
            events=events,
            total_coins=sum(event.coins for event in events),
            total_xp=sum(event.xp for event in events),
        )

    def apply_rewards(
        self, wallet: AtlasWallet, summary: RewardSummary
    ) -> AtlasWallet:
        """Return a new wallet with a reward summary applied."""
        mission_completed = any(
            event.reward_type is RewardType.MISSION_COMPLETE
            for event in summary.events
        )

        return AtlasWallet(
            xp=wallet.xp + summary.total_xp,
            coins=wallet.coins + summary.total_coins,
            lifetime_coins=wallet.lifetime_coins + summary.total_coins,
            momentum=wallet.momentum + 1 if mission_completed else wallet.momentum,
        )
