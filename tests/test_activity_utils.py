import unittest
from unittest.mock import MagicMock

from data.model.retirement_focus_type import RetirementFocusType
from data.model.state_type import StateType
from data.model.trait_type import TraitType
from domain.enums.activity_type import ActivityType
from domain.utils.activity_utils import (
    DEFAULT_ACTIVITY_WEIGHT,
    FREE_ACTIVITIES,
    INTENSE_PRACTICE_BASE_WEIGHT,
    compute_weights,
)
from tests.utils import create_blob_model_mock


def _trait(trait_type: TraitType):
    trait = MagicMock()
    trait.type = trait_type
    return trait


def _state(state_type: StateType):
    state = MagicMock()
    state.type = state_type
    return state


def _retirement_focus(focus_type: RetirementFocusType):
    focus = MagicMock()
    focus.focus_type = focus_type
    return focus


class TestActivityUtils(unittest.TestCase):
    def test_default_free_activity_weights(self):
        blob = create_blob_model_mock()
        blob.traits = []
        blob.states = []
        blob.retirement_focus = None

        weights = compute_weights(blob, FREE_ACTIVITIES)

        self.assertEqual(weights[ActivityType.PRACTICE], DEFAULT_ACTIVITY_WEIGHT)
        self.assertEqual(weights[ActivityType.LABOUR], DEFAULT_ACTIVITY_WEIGHT)
        self.assertEqual(weights[ActivityType.IDLE], DEFAULT_ACTIVITY_WEIGHT)
        self.assertEqual(weights[ActivityType.MINING], DEFAULT_ACTIVITY_WEIGHT)
        self.assertEqual(
            weights[ActivityType.INTENSE_PRACTICE], INTENSE_PRACTICE_BASE_WEIGHT
        )

    def test_retirement_focus_reduces_practice_weights(self):
        blob = create_blob_model_mock()
        blob.traits = []
        blob.states = []
        blob.retirement_focus = _retirement_focus(RetirementFocusType.LEGACY)

        weights = compute_weights(blob, FREE_ACTIVITIES)

        self.assertEqual(weights[ActivityType.PRACTICE], 0)
        self.assertEqual(weights[ActivityType.INTENSE_PRACTICE], 0)
        self.assertEqual(weights[ActivityType.LABOUR], DEFAULT_ACTIVITY_WEIGHT)

    def test_hard_working_doubles_labour_weight(self):
        blob = create_blob_model_mock()
        blob.traits = [_trait(TraitType.HARD_WORKING)]
        blob.states = []
        blob.retirement_focus = None

        weights = compute_weights(blob, FREE_ACTIVITIES)

        self.assertEqual(weights[ActivityType.LABOUR], DEFAULT_ACTIVITY_WEIGHT * 2)

    def test_determined_boosts_practice_and_intense_practice(self):
        blob = create_blob_model_mock()
        blob.traits = [_trait(TraitType.DETERMINED)]
        blob.states = []
        blob.retirement_focus = None

        weights = compute_weights(blob, FREE_ACTIVITIES)

        self.assertEqual(weights[ActivityType.PRACTICE], DEFAULT_ACTIVITY_WEIGHT * 2)
        self.assertEqual(weights[ActivityType.INTENSE_PRACTICE], 10)

    def test_lazy_reduces_training_weights(self):
        blob = create_blob_model_mock()
        blob.traits = [_trait(TraitType.LAZY)]
        blob.states = []
        blob.retirement_focus = None

        weights = compute_weights(blob, FREE_ACTIVITIES)

        self.assertEqual(weights[ActivityType.LABOUR], DEFAULT_ACTIVITY_WEIGHT / 2)
        self.assertEqual(weights[ActivityType.PRACTICE], DEFAULT_ACTIVITY_WEIGHT / 2)
        self.assertEqual(weights[ActivityType.INTENSE_PRACTICE], 0)

    def test_injured_disables_labour_and_intense_practice(self):
        blob = create_blob_model_mock()
        blob.traits = []
        blob.states = [_state(StateType.INJURED)]
        blob.retirement_focus = None

        weights = compute_weights(blob, FREE_ACTIVITIES)

        self.assertEqual(weights[ActivityType.LABOUR], 0)
        self.assertEqual(weights[ActivityType.PRACTICE], DEFAULT_ACTIVITY_WEIGHT / 2)
        self.assertEqual(weights[ActivityType.INTENSE_PRACTICE], 0)

    def test_gloomy_doubles_idle_weight(self):
        blob = create_blob_model_mock()
        blob.traits = []
        blob.states = [_state(StateType.GLOOMY)]
        blob.retirement_focus = None

        weights = compute_weights(blob, FREE_ACTIVITIES)

        self.assertEqual(weights[ActivityType.IDLE], DEFAULT_ACTIVITY_WEIGHT * 2)

    def test_administration_weight_adjustments(self):
        blob = create_blob_model_mock()
        blob.traits = [_trait(TraitType.DETERMINED), _trait(TraitType.LAZY)]
        blob.states = [_state(StateType.TIRED)]
        blob.retirement_focus = None

        weights = compute_weights(
            blob, FREE_ACTIVITIES + [ActivityType.ADMINISTRATION]
        )

        # 10 -> x2 (determined) -> /2+1 (lazy) -> /2 (tired)
        self.assertEqual(weights[ActivityType.ADMINISTRATION], 5.5)

    def test_prolonged_life_boosts_maintenance(self):
        blob = create_blob_model_mock()
        blob.traits = []
        blob.states = []
        blob.retirement_focus = _retirement_focus(
            RetirementFocusType.PROLONGED_LIFE
        )

        weights = compute_weights(blob, FREE_ACTIVITIES + [ActivityType.MAINTENANCE])

        self.assertEqual(weights[ActivityType.MAINTENANCE], DEFAULT_ACTIVITY_WEIGHT * 3)

    def test_legacy_boosts_apply_for_heir(self):
        blob = create_blob_model_mock()
        blob.traits = []
        blob.states = []
        blob.retirement_focus = _retirement_focus(RetirementFocusType.LEGACY)

        weights = compute_weights(
            blob, FREE_ACTIVITIES + [ActivityType.APPLY_FOR_HEIR]
        )

        self.assertEqual(
            weights[ActivityType.APPLY_FOR_HEIR], DEFAULT_ACTIVITY_WEIGHT * 5
        )

    def test_compute_weights_does_not_add_extra_activity_entries(self):
        blob = create_blob_model_mock()
        blob.traits = [
            _trait(TraitType.HARD_WORKING),
            _trait(TraitType.DETERMINED),
            _trait(TraitType.LAZY),
        ]
        blob.states = [
            _state(StateType.INJURED),
            _state(StateType.TIRED),
            _state(StateType.GLOOMY),
        ]
        blob.retirement_focus = _retirement_focus(RetirementFocusType.LEGACY)

        activities = [ActivityType.PRACTICE, ActivityType.IDLE]
        weights = compute_weights(blob, activities)

        self.assertEqual(set(weights.keys()), set(activities))
        self.assertEqual(len(weights), len(activities))


if __name__ == "__main__":
    unittest.main()
