import unittest
from unittest.mock import patch

from data.model.event_type import EventType
from domain.utils.event_utils import (
    EXCLUDED_EVENT_TYPES,
    build_random_event_type_sequence,
    get_allowed_event_types,
)


class TestEventUtils(unittest.TestCase):
    def test_excluded_event_types_are_not_allowed(self):
        allowed = get_allowed_event_types()
        for excluded in EXCLUDED_EVENT_TYPES:
            self.assertNotIn(excluded, allowed)

    def test_build_random_event_type_sequence_returns_empty_for_zero_count(self):
        self.assertEqual(build_random_event_type_sequence(0), [])

    def test_build_random_event_type_sequence_covers_all_allowed_when_enough_slots(self):
        allowed = get_allowed_event_types()
        sequence = build_random_event_type_sequence(len(allowed))
        self.assertEqual(len(sequence), len(allowed))
        self.assertEqual(set(sequence), set(allowed))

    def test_build_random_event_type_sequence_covers_all_allowed_with_extra_slots(self):
        allowed = get_allowed_event_types()
        sequence = build_random_event_type_sequence(len(allowed) + 3)
        self.assertEqual(len(sequence), len(allowed) + 3)
        self.assertTrue(set(allowed).issubset(set(sequence)))

    def test_build_random_event_type_sequence_samples_when_fewer_slots_than_types(self):
        allowed = get_allowed_event_types()
        sequence = build_random_event_type_sequence(len(allowed) - 1)
        self.assertEqual(len(sequence), len(allowed) - 1)
        self.assertEqual(len(set(sequence)), len(allowed) - 1)
        self.assertTrue(set(sequence).issubset(set(allowed)))

    @patch("domain.utils.event_utils.random.shuffle", lambda x: None)
    @patch("domain.utils.event_utils.random.choice", return_value=EventType.SPRINT_RACE)
    @patch("domain.utils.event_utils.random.sample", return_value=[EventType.ENDURANCE_RACE])
    def test_build_random_event_type_sequence_uses_sample_for_small_counts(
        self, mock_sample, mock_choice
    ):
        allowed = get_allowed_event_types()
        sequence = build_random_event_type_sequence(len(allowed) - 1)
        mock_sample.assert_called_once_with(allowed, len(allowed) - 1)
        self.assertEqual(sequence, [EventType.ENDURANCE_RACE])
        mock_choice.assert_not_called()


if __name__ == "__main__":
    unittest.main()
