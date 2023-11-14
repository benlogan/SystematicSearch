import unittest

from charting_keywords import extract_keyphrases
from parser import parse_file


class TestChartingKeywords(unittest.TestCase):

    # remember to change the working directory when executing this test, to the root of the project
    # otherwise all the relative path names will break

    def test_extract_phrases(self):
        data = parse_file('data/output/cleaned_dblp_1699956186.390304.bib')
        keywords = extract_keyphrases(data)
        self.assertEqual(2, keywords['green it'])

    def test_extract_phrases_groups(self):
        data = parse_file('data/output/cleaned_dblp_1699956186.390304.bib')
        keywords = extract_keyphrases(data)
        self.assertEqual(753, keywords['data center (group)'])

if __name__=='__main__':
	unittest.main()