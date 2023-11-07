import unittest

from bibtexparser.model import Entry, Field

from utility import find_duplicates


def create_mock_data():
    mock_data = []
    entry = Entry('article', 'Test2023', [Field("title", "test", 1)])
    mock_data.append(entry)
    return mock_data

def add_mock_data(title1, title2):
    mock_data = create_mock_data()

    entry = Entry('article', 'Test2023 a', [Field("title", title1, 1)])
    mock_data.append(entry)
    entry = Entry('article', 'Test2023 b', [Field("title", title2, 1)])
    mock_data.append(entry)

    return mock_data

class TestUtility(unittest.TestCase):

    def test_contains_something(self):
        self.assertEqual(len(find_duplicates(create_mock_data())), 1)

    def test_strip_characters(self):
        title1 = '''An Efficient NVM-Based Architecture for Intermittent Computing Under Energy Constraints'''
        title2 = '''An Efficient NVM based Architecture for Intermittent Computing Under Energy Constraints'''

        self.assertEqual(len(find_duplicates(add_mock_data(title1, title2))), 2)

    def test_special_characters(self):
        title1 = '''What makes research software sustainable?: an interview study with research software engineers'''
        title2 = '''What Makes Research Software Sustainable? An Interview Study With Research Software Engineers'''

        self.assertEqual(len(find_duplicates(add_mock_data(title1, title2))), 2)

    def test_strip_curly(self):
        title1 = '''{EACOF:} a framework for providing energy transparency to enable energy-aware software development'''
        title2 = '''{EACOF:} {A} Framework for Providing Energy Transparency to enable Energy-Aware Software Development'''

        self.assertEqual(len(find_duplicates(add_mock_data(title1, title2))), 2)

    def test_new_lines(self):
        title1 = '''{{EACOF:} {A} Framework for Providing Energy Transparency to enable
                          Energy-Aware Software Development}'''
        title2 = '''{{EACOF:} a framework for providing energy transparency to enable energy-aware
                          software development}'''

        self.assertEqual(len(find_duplicates(add_mock_data(title1, title2))), 2)

if __name__=='__main__':
	unittest.main()