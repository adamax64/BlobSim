from collections.abc import Callable
from dataclasses import dataclass

import random

from data.model.blob import Blob
from data.model.retirement_focus_type import RetirementFocusType
from data.model.state_type import StateType
from data.model.trait_type import TraitType
from domain.enums.activity_type import ActivityType
from domain.utils.blob_utils import has_state, has_trait

FREE_ACTIVITIES = [
    ActivityType.PRACTICE,
    ActivityType.LABOUR,
    ActivityType.IDLE,
    ActivityType.MINING,
    ActivityType.INTENSE_PRACTICE,
]

DEFAULT_ACTIVITY_WEIGHT = 10
INTENSE_OR_PREMIUM_PRACTICE_BASE_WEIGHT = 1
TRAIT_MULTIPLIER = 2
DETERMINED_INTENSE_PRACTICE_MULTIPLIER = 10
PROLONGED_LIFE_MAINTENANCE_MULTIPLIER = 3
LEGACY_HEIR_MULTIPLIER = 5

DEFAULT_FREE_BASE_WEIGHTS: dict[ActivityType, float] = {
    ActivityType.PRACTICE: DEFAULT_ACTIVITY_WEIGHT,
    ActivityType.LABOUR: DEFAULT_ACTIVITY_WEIGHT,
    ActivityType.IDLE: DEFAULT_ACTIVITY_WEIGHT,
    ActivityType.MINING: DEFAULT_ACTIVITY_WEIGHT,
    ActivityType.INTENSE_PRACTICE: INTENSE_OR_PREMIUM_PRACTICE_BASE_WEIGHT,
}

RETIREMENT_FOCUS_FREE_BASE_WEIGHTS: dict[ActivityType, float] = {
    ActivityType.PRACTICE: 0,
    ActivityType.LABOUR: DEFAULT_ACTIVITY_WEIGHT,
    ActivityType.IDLE: DEFAULT_ACTIVITY_WEIGHT,
    ActivityType.MINING: DEFAULT_ACTIVITY_WEIGHT,
    ActivityType.INTENSE_PRACTICE: 0,
}


@dataclass(frozen=True)
class WeightRule:
    condition: Callable[[Blob], bool]
    adjustments: dict[ActivityType, Callable[[float], float]]


def _multiply(factor: float) -> Callable[[float], float]:
    return lambda weight: weight * factor


def _divide(factor: float) -> Callable[[float], float]:
    return lambda weight: weight / factor


def _set(weight: float) -> Callable[[float], float]:
    return lambda _: weight


def _lazy_administration(weight: float) -> float:
    return weight / 2 + 1


EXTRA_ACTIVITY_RULES: list[WeightRule] = [
    WeightRule(
        condition=lambda blob: has_trait(blob, TraitType.DETERMINED),
        adjustments={ActivityType.ADMINISTRATION: _multiply(TRAIT_MULTIPLIER)},
    ),
    WeightRule(
        condition=lambda blob: has_trait(blob, TraitType.LAZY),
        adjustments={ActivityType.ADMINISTRATION: _lazy_administration},
    ),
    WeightRule(
        condition=lambda blob: has_state(blob, StateType.TIRED)
        or has_state(blob, StateType.GLOOMY),
        adjustments={ActivityType.ADMINISTRATION: _divide(TRAIT_MULTIPLIER)},
    ),
    WeightRule(
        condition=lambda blob: (
            blob.retirement_focus is not None
            and blob.retirement_focus.focus_type == RetirementFocusType.PROLONGED_LIFE
        ),
        adjustments={
            ActivityType.MAINTENANCE: _multiply(PROLONGED_LIFE_MAINTENANCE_MULTIPLIER)
        },
    ),
    WeightRule(
        condition=lambda blob: (
            blob.retirement_focus is not None
            and blob.retirement_focus.focus_type == RetirementFocusType.LEGACY
        ),
        adjustments={ActivityType.APPLY_FOR_HEIR: _multiply(LEGACY_HEIR_MULTIPLIER)},
    ),
    WeightRule(
        condition=lambda blob: has_trait(blob, TraitType.DETERMINED),
        adjustments={ActivityType.PREMIUM_PRACTICE: _multiply(TRAIT_MULTIPLIER)},
    ),
]

FREE_ACTIVITY_RULES: list[WeightRule] = [
    WeightRule(
        condition=lambda blob: has_trait(blob, TraitType.HARD_WORKING),
        adjustments={ActivityType.LABOUR: _multiply(TRAIT_MULTIPLIER)},
    ),
    WeightRule(
        condition=lambda blob: has_trait(blob, TraitType.DETERMINED),
        adjustments={
            ActivityType.PRACTICE: _multiply(TRAIT_MULTIPLIER),
            ActivityType.INTENSE_PRACTICE: _multiply(
                DETERMINED_INTENSE_PRACTICE_MULTIPLIER
            ),
        },
    ),
    WeightRule(
        condition=lambda blob: has_trait(blob, TraitType.LAZY),
        adjustments={
            ActivityType.LABOUR: _divide(TRAIT_MULTIPLIER),
            ActivityType.PRACTICE: _divide(TRAIT_MULTIPLIER),
            ActivityType.INTENSE_PRACTICE: _set(0),
        },
    ),
    WeightRule(
        condition=lambda blob: has_state(blob, StateType.INJURED),
        adjustments={
            ActivityType.LABOUR: _set(0),
            ActivityType.PRACTICE: _divide(TRAIT_MULTIPLIER),
            ActivityType.INTENSE_PRACTICE: _set(0),
        },
    ),
    WeightRule(
        condition=lambda blob: has_state(blob, StateType.TIRED),
        adjustments={
            ActivityType.PRACTICE: _divide(TRAIT_MULTIPLIER),
            ActivityType.INTENSE_PRACTICE: _set(0),
        },
    ),
    WeightRule(
        condition=lambda blob: has_state(blob, StateType.GLOOMY),
        adjustments={ActivityType.IDLE: _multiply(TRAIT_MULTIPLIER)},
    ),
]


def choose_activity(
    blob: Blob,
    extra_activities: list[ActivityType] | None = None,
    free_premium_practice: bool = False,
) -> ActivityType:
    """Choose an activity for `blob` with weights adjusted by traits and states."""
    activities = FREE_ACTIVITIES + (extra_activities or [])
    weights = compute_weights(blob, activities, free_premium_practice)
    return random.choices(
        activities, weights=[weights[activity] for activity in activities], k=1
    )[0]


def compute_weights(
    blob: Blob, activities: list[ActivityType], free_premium_practice: bool
) -> dict[ActivityType, float]:
    """Compute final activity weights for the given activity pool."""
    weights = _get_initial_weights(blob, activities, free_premium_practice)
    _apply_rules(blob, weights, EXTRA_ACTIVITY_RULES)
    _apply_rules(blob, weights, FREE_ACTIVITY_RULES)
    return weights


def _get_initial_weights(
    blob: Blob, activities: list[ActivityType], free_premium_practice: bool
) -> dict[ActivityType, float]:
    base_weights = (
        RETIREMENT_FOCUS_FREE_BASE_WEIGHTS
        if blob.retirement_focus is not None
        else DEFAULT_FREE_BASE_WEIGHTS
    )

    weights: dict[ActivityType, float] = {}
    for activity in activities:
        if activity == ActivityType.PREMIUM_PRACTICE:
            weights[activity] = (
                DEFAULT_ACTIVITY_WEIGHT
                if free_premium_practice
                else INTENSE_OR_PREMIUM_PRACTICE_BASE_WEIGHT
            )
        elif activity == ActivityType.PRACTICE:
            weights[activity] = (
                0
                if free_premium_practice
                else base_weights.get(activity, DEFAULT_ACTIVITY_WEIGHT)
            )
        else:
            weights[activity] = base_weights.get(activity, DEFAULT_ACTIVITY_WEIGHT)
    return weights


def _apply_rules(
    blob: Blob,
    weights: dict[ActivityType, float],
    rules: list[WeightRule],
) -> None:
    for rule in rules:
        if not rule.condition(blob):
            continue
        for activity, adjust in rule.adjustments.items():
            if activity in weights:
                weights[activity] = adjust(weights[activity])
