import unittest
from unittest.mock import patch, MagicMock

from domain.competition_service import process_event_results
from domain.dtos.event_dto import EventDto
from domain.utils.blob_name_utils import format_blob_name
from tests.utils import create_blob_model_mock, create_mock_blob_competitor
from tests.utils import create_mock_result


class TestProcessEventResults(unittest.TestCase):

    @patch('domain.competition_service.add_event_ended_news')
    @patch('domain.competition_service.conclude_calendar_event')
    @patch('domain.competition_service.save_all_blobs')
    @patch('domain.competition_service.save_all_results')
    def test_process_event_results_quartered_event_records(
        self,
        mock_save_all_results,
        mock_save_all_blobs,
        mock_conclude_calendar_event,
        mock_add_event_ended_news
    ):
        mock_blob_competitor1 = create_mock_blob_competitor(id=1, points=0, gold_trophies=0, name='Blob1')
        mock_blob_competitor2 = create_mock_blob_competitor(id=2, points=0, gold_trophies=0, name='Blob2')
        mock_blob_competitor3 = create_mock_blob_competitor(id=3, points=0, gold_trophies=0, name='Blob3')

        mock_league = MagicMock()
        mock_league.level = 1
        mock_league.name = 'Masters League'

        event = EventDto(
            id=123,
            competitors=[],
            actions=[],
            league=mock_league,
            season=2025,
            round=5,
            type=None,
            isFinished=False
        )

        from domain.dtos.event_record_dto import QuarteredEventRecordDto, ScoreDto
        quarters1 = [
            ScoreDto(score=1.0, best=False),
            ScoreDto(score=3.0, best=True),
            ScoreDto(score=1.0, best=False),
            ScoreDto(score=3.0, best=True)
        ]
        quarters2 = [
            ScoreDto(score=2.5, best=True),
            ScoreDto(score=2.5, best=False),
            ScoreDto(score=2.5, best=True),
            ScoreDto(score=2.5, best=False)
        ]
        quarters3 = [
            ScoreDto(score=2.0, best=False),
            ScoreDto(score=2.0, best=False),
            ScoreDto(score=2.0, best=False),
            ScoreDto(score=2.0, best=False)
        ]

        record1 = QuarteredEventRecordDto(blob=mock_blob_competitor1, quarters=quarters1)
        record2 = QuarteredEventRecordDto(blob=mock_blob_competitor2, quarters=quarters2)
        record3 = QuarteredEventRecordDto(blob=mock_blob_competitor3, quarters=quarters3)
        event_records = [record1, record2, record3]

        mock_blob1 = create_blob_model_mock(first_name='John', last_name='Doe', id=mock_blob_competitor1.id)
        mock_blob2 = create_blob_model_mock(first_name='Jane', last_name='Doe', id=mock_blob_competitor2.id)
        mock_blob3 = create_blob_model_mock(first_name='Test', last_name='Blob', id=mock_blob_competitor3.id)

        mock_result1 = create_mock_result(1, mock_blob1, 6, event.id, mock_blob1.id)
        mock_result2 = create_mock_result(2, mock_blob2, 4, event.id, mock_blob2.id)
        mock_result3 = create_mock_result(3, mock_blob3, 1, event.id, mock_blob3.id)
        saved_results = [mock_result1, mock_result2, mock_result3]
        mock_save_all_results.return_value = saved_results

        session = MagicMock()

        process_event_results(event, event_records, session)

        # Assert save_all_results called with correct params
        mock_save_all_results.assert_called_once()
        args, _ = mock_save_all_results.call_args
        self.assertEqual(args[0], session)
        self.assertIsInstance(args[1], list)
        actual_results = args[1]
        expected = [
            (1, mock_blob_competitor1.id, 6),
            (2, mock_blob_competitor2.id, 4),
            (3, mock_blob_competitor3.id, 1)
        ]
        self.assertEqual(len(actual_results), 3)
        for result, (exp_pos, exp_blob_id, exp_points) in zip(actual_results, expected):
            self.assertEqual(result.position, exp_pos)
            self.assertEqual(result.blob_id, exp_blob_id)
            self.assertEqual(result.points, exp_points)

        # Assert save_all_blobs called with correct params
        mock_save_all_blobs.assert_called_once()
        blobs_arg = mock_save_all_blobs.call_args[0][1]
        self.assertTrue(all(hasattr(b, 'id') for b in blobs_arg))
        self.assertEqual({b.id for b in blobs_arg}, {1, 2, 3})

        # Assert conclude_calendar_event called with correct params
        mock_conclude_calendar_event.assert_called_once_with(session)

        # Assert add_event_ended_news called with correct params
        mock_add_event_ended_news.assert_called_once()
        news_args = mock_add_event_ended_news.call_args[0]
        self.assertEqual(news_args[0], mock_league.name)
        self.assertEqual(news_args[1], event.round)
        self.assertEqual(news_args[2], format_blob_name(mock_blob1))
        self.assertEqual(news_args[3], format_blob_name(mock_blob2))
        self.assertEqual(news_args[4], format_blob_name(mock_blob3))
        self.assertEqual(news_args[5], session)

    if __name__ == '__main__':
        unittest.main()
