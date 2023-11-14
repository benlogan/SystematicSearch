import unittest

from bibtexparser.model import Entry, Field

from charting_keywords import extract_keyphrases
from parser import parse_file


class TestChartingKeywords(unittest.TestCase):

    # remember to change the working directory when executing this test, to the root of the project
    # otherwise all the relative path names will break

    def test_extract_phrases(self):
        data = parse_file('data/output/cleaned_dblp_1699956186.390304.bib')
        keywords = extract_keyphrases(data.entries)
        self.assertEqual(2, keywords['green it'])

    def test_extract_phrases_groups(self):
        data = parse_file('data/output/cleaned_dblp_1699956186.390304.bib')
        keywords = extract_keyphrases(data.entries)
        self.assertEqual(426, keywords['data center (*)'])

    def test_data_centre(self):
        data = []
        entry = Entry('article', 'Test2023a', [Field("title", "a paper about a data center", 1)])
        data.append(entry)
        entry = Entry('article', 'Test2023b', [Field("title", "all about data centres", 1)])
        data.append(entry)
        entry = Entry('article', 'Test2023c', [Field("title", "nothing to do with DCs", 1)])
        data.append(entry)
        entry = Entry('article', 'Test2023d', [Field("title", "something to do with datacentres", 1)])
        data.append(entry)
        entry = Entry('article', 'Test2023e', [Field("title", "yet another datacenter paper", 1)])
        data.append(entry)
        keywords = extract_keyphrases(data)
        self.assertEqual(4, keywords['data center (*)'])

    def test_phrase_repetition(self):
        data = []
        entry = Entry('article', 'Test2023a', [Field("title", "a cloud paper about the cloud, written in the cloud with cloud computing", 1)])
        data.append(entry)
        entry = Entry('article', 'Test2023b', [Field("title", "all about something", 1)])
        data.append(entry)
        entry = Entry('article', 'Test2023c', [Field("title", "nothing to do with this", 1)])
        data.append(entry)
        keywords = extract_keyphrases(data)
        self.assertEqual(1, keywords['cloud (*)'])

    def test_double_counting(self):
        data = []
        entry = Entry('article', 'Test2023a', [Field("title", "a paper on cloud", 1)])
        data.append(entry)
        entry = Entry('article', 'Test2023b', [Field("title", "all about cloud computing", 1)])
        data.append(entry)
        entry = Entry('article', 'Test2023c', [Field("title", "nothing to do with the sky", 1)])
        data.append(entry)
        entry = Entry('article', 'Test2023d', [Field("title", "test", 1)])
        data.append(entry)
        keywords = extract_keyphrases(data)
        self.assertEqual(2, keywords['cloud (*)'])

    def test_multiple_hits(self):
        data = []
        entry = Entry('article', 'Test2023a', [Field("title", "a paper on cloud", 1)])
        data.append(entry)
        entry = Entry('article', 'Test2023b', [Field("title", "all about computing", 1)])
        data.append(entry)
        entry = Entry('article', 'Test2023c', [Field("title", "nothing to do with the sky", 1)])
        data.append(entry)
        entry = Entry('article', 'Test2023d', [Field("title", "a cloud mapping study", 1)])
        data.append(entry)
        keywords = extract_keyphrases(data)
        self.assertEqual(2, keywords['cloud (*)'])
        self.assertEqual(1, keywords['mapping study'])

if __name__=='__main__':
	unittest.main()