import unittest

from bibtexparser.model import Entry, Field

from search import SEARCH_STRING, reapply_search


def create_mock_data():
    mock_data = []
    mock_data.append(Entry('article', 'Test2023', [Field("title", "Managing green IT", 1)]))
    mock_data.append(Entry('article', 'Test2023a', [Field("title", "Managing Green IT", 1)]))
    mock_data.append(Entry('article', 'Test2023b', [Field("title", "Managing green it is cool", 1)]))
    mock_data.append(Entry('article', 'Test2023c', [Field("title", "cloud it sure is something", 1)]))
    mock_data.append(Entry('article', 'Test2023d', [Field("title", "energy it really is great", 1)]))
    mock_data.append(Entry('article', 'Test2024', [Field("title", "energy and the cloud", 1)]))
    mock_data.append(Entry('article', 'Test2025', [Field("title", "just a random test with no match", 1)]))
    mock_data.append(Entry('article', 'Test2025a', [Field("title", "just a random test with one match : computing", 1)]))
    mock_data.append(Entry('article', 'Test2026', [Field("title", "software words in between keywords sustainable", 1)]))
    mock_data.append(Entry('article', 'Test2027', [Field("title", "SUSTAINABLE software", 1)]))
    return mock_data


class TestSearch(unittest.TestCase):

    def test_query(self):
        data = create_mock_data()
        self.assertEqual(5, len(reapply_search(data, SEARCH_STRING, True)))