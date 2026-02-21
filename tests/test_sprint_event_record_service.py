import unittest

from domain.event_record_services.race_event_records_service import (
    get_sprint_event_records,
)
from domain.dtos.action_dto import ActionDto
from domain.dtos.blob_competitor_dto import BlobCompetitorDto


class TestSprintEventRecordService(unittest.TestCase):

    def test_sprint_finish_different_ticks(self):
        """Blob1 finishes at tick 0, Blob2 finishes at tick 1"""
        competitors = [
            BlobCompetitorDto(
                id=1, name="Blob1", color="#FF0000", strength=1.0, speed=1.0, states=[]
            ),
            BlobCompetitorDto(
                id=2, name="Blob2", color="#00FF00", strength=1.0, speed=1.0, states=[]
            ),
        ]

        # race_length for 2 competitors is 60 (from league utils)
        actions = [
            ActionDto(blob_id=1, scores=[60]),  # finishes at tick 0
            ActionDto(blob_id=2, scores=[30, 40]),  # finishes at tick 1
        ]

        records = get_sprint_event_records(actions, competitors, is_playback=False)

        self.assertEqual(records[0].blob.id, 1)  # Blob1 finished earlier
        self.assertEqual(records[1].blob.id, 2)
        # both should be marked finished and have their fractional times
        self.assertTrue(records[0].is_finished)
        self.assertTrue(records[1].is_finished)
        self.assertAlmostEqual(records[0].time, 1.0)
        self.assertAlmostEqual(records[1].time, 1.75)

    def test_sprint_same_tick_tiebreaker(self):
        """Both finish in same tick; tie-breaker by (remaining / score) ascending"""
        competitors = [
            BlobCompetitorDto(
                id=1, name="Blob1", color="#FF0000", strength=1.0, speed=1.0, states=[]
            ),
            BlobCompetitorDto(
                id=2, name="Blob2", color="#00FF00", strength=1.0, speed=1.0, states=[]
            ),
        ]

        # Both finish at tick 1. Compute remaining/time:
        # Blob1: tick0=30, tick1 score=40 -> remaining=60-30=30 -> time=30/40=0.75
        # Blob2: tick0=50, tick1 score=20 -> remaining=60-50=10 -> time=10/20=0.5 -> Blob2 earlier
        actions = [
            ActionDto(blob_id=1, scores=[30, 40]),
            ActionDto(blob_id=2, scores=[50, 20]),
        ]

        records = get_sprint_event_records(actions, competitors, is_playback=False)

        self.assertEqual(records[0].blob.id, 2)
        self.assertEqual(records[1].blob.id, 1)
        # both should be marked finished and have times reflecting tie-breaker
        self.assertTrue(records[0].is_finished)
        self.assertTrue(records[1].is_finished)
        self.assertAlmostEqual(records[0].time, 1.5)
        self.assertAlmostEqual(records[1].time, 1.75)

    def test_sprint_non_finisher_time_none(self):
        """A blob that doesn't reach the race length should not be finished and have no time."""
        competitors = [
            BlobCompetitorDto(
                id=1, name="Blob1", color="#FF0000", strength=1.0, speed=1.0, states=[]
            ),
            BlobCompetitorDto(
                id=2, name="Blob2", color="#00FF00", strength=1.0, speed=1.0, states=[]
            ),
        ]

        actions = [
            ActionDto(blob_id=1, scores=[30, 20]),  # total 50 -> not finished
            ActionDto(blob_id=2, scores=[60]),  # finished
        ]

        records = get_sprint_event_records(actions, competitors, is_playback=False)

        rec1 = next(r for r in records if r.blob.id == 1)
        rec2 = next(r for r in records if r.blob.id == 2)

        self.assertFalse(rec1.is_finished)
        self.assertIsNone(rec1.time)
        self.assertTrue(rec2.is_finished)
        self.assertAlmostEqual(rec2.time, 1.0)


if __name__ == "__main__":
    unittest.main()
