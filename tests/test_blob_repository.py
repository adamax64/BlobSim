import unittest
from unittest.mock import MagicMock

from data.model.blob import Blob
from data.persistence.blob_repository import get_labouring_blob_count


class TestBlobRepository(unittest.TestCase):
    def test_get_labouring_blob_count(self):
        session = MagicMock()
        session.query.return_value.filter.return_value.count.return_value = 7

        result = get_labouring_blob_count(session)

        self.assertEqual(result, 7)
        session.query.assert_called_once_with(Blob)
        session.query.return_value.filter.return_value.count.assert_called_once_with()
