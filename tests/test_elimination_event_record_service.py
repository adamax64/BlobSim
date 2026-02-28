import unittest

from domain.event_record_services.elimination_event_record_service import (
    get_elimination_event_records,
)
from domain.dtos.action_dto import ActionDto
from domain.dtos.blob_competitor_dto import BlobCompetitorDto


class TestEliminationEventRecordService(unittest.TestCase):

    def test_get_elimination_event_records_no_actions(self):
        """Test elimination event records when no actions exist (tick 0)"""
        competitors = [
            BlobCompetitorDto(
                id=1, name="Blob1", color="#FF0000", strength=1.0, speed=1.0, states=[]
            ),
            BlobCompetitorDto(
                id=2, name="Blob2", color="#00FF00", strength=1.0, speed=1.0, states=[]
            ),
            BlobCompetitorDto(
                id=3, name="Blob3", color="#0000FF", strength=1.0, speed=1.0, states=[]
            ),
        ]
        actions = []

        records = get_elimination_event_records(actions, competitors)

        self.assertEqual(len(records), 3)
        for i, record in enumerate(records):
            self.assertEqual(record.blob.id, competitors[i].id)
            self.assertIsNone(record.last_score)
            self.assertFalse(record.eliminated)
            self.assertEqual(record.tick_wins, 0)

    def test_get_elimination_event_records_single_tick(self):
        """Test elimination event records with one tick completed"""
        competitors = [
            BlobCompetitorDto(
                id=1, name="Blob1", color="#FF0000", strength=1.0, speed=1.0, states=[]
            ),
            BlobCompetitorDto(
                id=2, name="Blob2", color="#00FF00", strength=1.0, speed=1.0, states=[]
            ),
            BlobCompetitorDto(
                id=3, name="Blob3", color="#0000FF", strength=1.0, speed=1.0, states=[]
            ),
        ]

        # Blob1 wins first tick with score 0.9, Blob2 gets 0.7, Blob3 gets 0.5
        actions = [
            ActionDto(blob_id=1, scores=[0.9]),
            ActionDto(blob_id=2, scores=[0.7]),
            ActionDto(blob_id=3, scores=[0.5]),
        ]

        records = get_elimination_event_records(actions, competitors)

        self.assertEqual(len(records), 3)

        # Records should be sorted by score (highest first)
        self.assertEqual(records[0].blob.id, 1)  # Winner
        self.assertEqual(records[0].last_score, 0.9)
        self.assertFalse(records[0].eliminated)
        self.assertEqual(records[0].tick_wins, 1)  # Won the tick

        self.assertEqual(records[1].blob.id, 2)  # Second place
        self.assertEqual(records[1].last_score, 0.7)
        self.assertFalse(records[1].eliminated)
        self.assertEqual(records[1].tick_wins, 0)  # Didn't win

        self.assertEqual(records[2].blob.id, 3)  # Last place (eliminated)
        self.assertEqual(records[2].last_score, 0.5)
        self.assertTrue(records[2].eliminated)  # Should be eliminated
        self.assertEqual(records[2].tick_wins, 0)  # Didn't win

    def test_get_elimination_event_records_multiple_ticks(self):
        """Test elimination event records with multiple ticks"""
        competitors = [
            BlobCompetitorDto(
                id=1, name="Blob1", color="#FF0000", strength=1.0, speed=1.0, states=[]
            ),
            BlobCompetitorDto(
                id=2, name="Blob2", color="#00FF00", strength=1.0, speed=1.0, states=[]
            ),
            BlobCompetitorDto(
                id=3, name="Blob3", color="#0000FF", strength=1.0, speed=1.0, states=[]
            ),
            BlobCompetitorDto(
                id=4, name="Blob4", color="#FFFF00", strength=1.0, speed=1.0, states=[]
            ),
        ]

        # Tick 1: Blob1 wins (0.9), Blob2 (0.7), Blob3 (0.5), Blob4 (0.3) - Blob4 eliminated
        # Tick 2: Blob1 wins (0.8), Blob2 (0.6), Blob3 (0.4) - Blob3 eliminated
        # Tick 3: Blob1 wins (0.7), Blob2 (0.5) - Blob2 eliminated
        actions = [
            ActionDto(blob_id=1, scores=[0.9, 0.8, 0.7]),  # Won all 3 ticks
            ActionDto(blob_id=2, scores=[0.7, 0.6, 0.5]),  # Won 0 ticks
            ActionDto(
                blob_id=3, scores=[0.5, 0.4]
            ),  # Won 0 ticks, eliminated after tick 2
            ActionDto(blob_id=4, scores=[0.3]),  # Won 0 ticks, eliminated after tick 1
        ]

        records = get_elimination_event_records(actions, competitors)

        self.assertEqual(len(records), 4)

        # Records should be sorted by current tick score (highest first)
        self.assertEqual(records[0].blob.id, 1)  # Winner
        self.assertEqual(records[0].last_score, 0.7)
        self.assertFalse(records[0].eliminated)
        self.assertEqual(records[0].tick_wins, 3)  # Won all 3 ticks

        # The production code marks the last current_tick records as eliminated
        # So records[1], records[2], and records[3] should all be eliminated
        self.assertEqual(records[1].blob.id, 2)  # Second place
        self.assertEqual(records[1].last_score, 0.5)
        self.assertTrue(
            records[1].eliminated
        )  # Marked as eliminated by production logic
        self.assertEqual(records[1].tick_wins, 0)  # Won 0 ticks

        self.assertEqual(records[2].blob.id, 3)  # Third place (eliminated)
        self.assertEqual(records[2].last_score, None)
        self.assertTrue(
            records[2].eliminated
        )  # Marked as eliminated by production logic
        self.assertEqual(records[2].tick_wins, 0)  # Won 0 ticks

        self.assertEqual(records[3].blob.id, 4)  # Fourth place (eliminated)
        self.assertEqual(records[3].last_score, None)
        self.assertTrue(
            records[3].eliminated
        )  # Marked as eliminated by production logic
        self.assertEqual(records[3].tick_wins, 0)  # Won 0 ticks

    def test_get_elimination_event_records_tie_in_tick(self):
        """Test elimination event records when there's a tie in a tick"""
        competitors = [
            BlobCompetitorDto(
                id=1, name="Blob1", color="#FF0000", strength=1.0, speed=1.0, states=[]
            ),
            BlobCompetitorDto(
                id=2, name="Blob2", color="#00FF00", strength=1.0, speed=1.0, states=[]
            ),
            BlobCompetitorDto(
                id=3, name="Blob3", color="#0000FF", strength=1.0, speed=1.0, states=[]
            ),
        ]

        # Tick 1: Blob1 and Blob2 tie with 0.8, Blob3 gets 0.5
        # In case of tie, max() will pick the first one (Blob1)
        actions = [
            ActionDto(blob_id=1, scores=[0.8]),
            ActionDto(blob_id=2, scores=[0.8]),
            ActionDto(blob_id=3, scores=[0.5]),
        ]

        records = get_elimination_event_records(actions, competitors)

        self.assertEqual(len(records), 3)

        # Blob1 should win the tick due to tie-breaking
        self.assertEqual(records[0].blob.id, 1)
        self.assertEqual(records[0].tick_wins, 1)

        self.assertEqual(records[1].blob.id, 2)
        self.assertEqual(records[1].tick_wins, 0)  # Lost due to tie-breaking

        self.assertEqual(records[2].blob.id, 3)
        self.assertEqual(records[2].tick_wins, 0)

    def test_get_elimination_event_records_missing_competitor(self):
        """Test elimination event records when action references non-existent competitor"""
        competitors = [
            BlobCompetitorDto(
                id=1, name="Blob1", color="#FF0000", strength=1.0, speed=1.0, states=[]
            ),
            BlobCompetitorDto(
                id=2, name="Blob2", color="#00FF00", strength=1.0, speed=1.0, states=[]
            ),
        ]

        # Action for blob_id=3 which doesn't exist in competitors
        actions = [
            ActionDto(blob_id=1, scores=[0.9]),
            ActionDto(blob_id=2, scores=[0.7]),
            ActionDto(blob_id=3, scores=[0.5]),  # This competitor doesn't exist
        ]

        records = get_elimination_event_records(actions, competitors)

        # Should return records for all actions, including non-existent competitors
        self.assertEqual(len(records), 3)

        # The missing competitor should be handled gracefully (blob will be None)
        for record in records:
            if record.blob is not None:
                self.assertIn(record.blob.id, [1, 2])
            else:
                # This is the record for the missing competitor
                self.assertIsNone(record.blob)

    def test_get_elimination_event_records_empty_competitors(self):
        """Test elimination event records with empty competitors list"""
        competitors = []
        actions = []

        records = get_elimination_event_records(actions, competitors)

        self.assertEqual(len(records), 0)

    def test_get_elimination_event_records_complex_scenario(self):
        """Test a complex scenario with multiple eliminations and different winners"""
        competitors = [
            BlobCompetitorDto(
                id=1, name="Blob1", color="#FF0000", strength=1.0, speed=1.0, states=[]
            ),
            BlobCompetitorDto(
                id=2, name="Blob2", color="#00FF00", strength=1.0, speed=1.0, states=[]
            ),
            BlobCompetitorDto(
                id=3, name="Blob3", color="#0000FF", strength=1.0, speed=1.0, states=[]
            ),
            BlobCompetitorDto(
                id=4, name="Blob4", color="#FFFF00", strength=1.0, speed=1.0, states=[]
            ),
            BlobCompetitorDto(
                id=5, name="Blob5", color="#FF00FF", strength=1.0, speed=1.0, states=[]
            ),
        ]

        # Tick 1: Blob2 wins (0.9), Blob1 (0.8), Blob3 (0.7), Blob4 (0.6), Blob5 (0.5) - Blob5 eliminated
        # Tick 2: Blob1 wins (0.8), Blob2 (0.7), Blob3 (0.6), Blob4 (0.5) - Blob4 eliminated
        # Tick 3: Blob3 wins (0.7), Blob1 (0.6), Blob2 (0.5) - Blob2 eliminated
        # Tick 4: Blob1 wins (0.6), Blob3 (0.5) - Blob3 eliminated
        actions = [
            ActionDto(blob_id=1, scores=[0.8, 0.8, 0.6, 0.6]),  # Won ticks 2, 4
            ActionDto(blob_id=2, scores=[0.9, 0.7, 0.5]),  # Won tick 1
            ActionDto(blob_id=3, scores=[0.7, 0.6, 0.7, 0.5]),  # Won tick 3
            ActionDto(blob_id=4, scores=[0.6, 0.5]),  # Won 0 ticks
            ActionDto(blob_id=5, scores=[0.5]),  # Won 0 ticks
        ]

        records = get_elimination_event_records(actions, competitors)

        self.assertEqual(len(records), 5)

        # Check tick wins
        tick_wins_by_blob = {record.blob.id: record.tick_wins for record in records}
        self.assertEqual(tick_wins_by_blob[1], 2)  # Won ticks 2, 4
        self.assertEqual(tick_wins_by_blob[2], 1)  # Won tick 1
        self.assertEqual(tick_wins_by_blob[3], 1)  # Won tick 3
        self.assertEqual(tick_wins_by_blob[4], 0)  # Won 0 ticks
        self.assertEqual(tick_wins_by_blob[5], 0)  # Won 0 ticks

        # Check elimination status
        elimination_status = {record.blob.id: record.eliminated for record in records}
        self.assertFalse(elimination_status[1])  # Winner
        self.assertTrue(elimination_status[2])  # Eliminated
        self.assertTrue(elimination_status[3])  # Eliminated
        self.assertTrue(elimination_status[4])  # Eliminated
        self.assertTrue(elimination_status[5])  # Eliminated


if __name__ == "__main__":
    unittest.main()
