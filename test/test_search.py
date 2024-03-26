import unittest

from bibtexparser.model import Entry, Field

from search import SEARCH_STRING, reapply_search


def create_mock_data():
    mock_data = []
    entry = Entry('article', 'Test2023', [Field("title", "Managing Green IT", 1)])
    mock_data.append(entry)
    return mock_data


class TestSearch(unittest.TestCase):
    def test_basic_search(self):
        data = create_mock_data()
        self.assertEqual(len(data), len(reapply_search(data, SEARCH_STRING, True)))