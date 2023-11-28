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
        self.assertEqual(1, len(find_duplicates(create_mock_data())))

    def test_strip_characters(self):
        title1 = '''An Efficient NVM-Based Architecture for Intermittent Computing Under Energy Constraints'''
        title2 = '''An Efficient NVM based Architecture for Intermittent Computing Under Energy Constraints'''

        self.assertEqual(2, len(find_duplicates(add_mock_data(title1, title2))))

    def test_special_characters(self):
        title1 = '''What makes research software sustainable?: an interview study with research software engineers'''
        title2 = '''What Makes Research Software Sustainable? An Interview Study With Research Software Engineers'''

        self.assertEqual(2, len(find_duplicates(add_mock_data(title1, title2))))

    def test_more_special_characters(self):
        title1 = '''The ‘Vattn’ Case: Analysing Sustainability Impacts in a Software Startup'''
        title2 = '''The 'Vattn' Case: Analysing Sustainability Impacts in a Software Startup'''

        self.assertEqual(2, len(find_duplicates(add_mock_data(title1, title2))))

    def test_strip_curly(self):
        title1 = '''{EACOF:} a framework for providing energy transparency to enable energy-aware software development'''
        title2 = '''{EACOF:} {A} Framework for Providing Energy Transparency to enable Energy-Aware Software Development'''

        self.assertEqual(2, len(find_duplicates(add_mock_data(title1, title2))))

    # FIXME still working here - quite fiddly - is this worth it, for one problem case!?
    # def test_tricky(self):
    #     title1 = '''Spintastic: Spin-based stochastic logic for energy-efficient computing'''
    #     title2 = '''Spintastic: {\\textless}u{\\textgreater}spin{\\textless}/u{\\textgreater}-based
    #               s{\\textless}u{\\textgreater}t{\\textless}/u{\\textgreater}och{\\textless}u{\\textgreater}astic{\\textless}/u{\\textgreater}
    #               logic for energy-efficient computing'''
    #     #title3 = '''Spintastic: &lt;u&gt;spin&lt;/U&gt;-Based S&lt;u&gt;t&lt;/U&gt;och&lt;u&gt;astic&lt;/U&gt; Logic for Energy-Efficient Computing'''
    #     self.assertEqual(2, len(find_duplicates(add_mock_data(title1, title2))))

    def test_new_lines(self):
        title1 = '''{{EACOF:} {A} Framework for Providing Energy Transparency to enable
                          Energy-Aware Software Development}'''
        title2 = '''{{EACOF:} a framework for providing energy transparency to enable energy-aware
                          software development}'''

        self.assertEqual(2, len(find_duplicates(add_mock_data(title1, title2))))

    # already handle this, but replace with blank space. probably need to test equality with no whitespace
    def test_more_characters(self):
        title1 = '''FPnew: An Open-Source Multi-Format Floating-Point Unit Architecture for Energy-Proportional Transprecision Computing'''
        title2 = '''FPnew: An Open-Source Multiformat Floating-Point Unit Architecture for Energy-Proportional Transprecision Computing'''

        self.assertEqual(2, len(find_duplicates(add_mock_data(title1, title2))))

    def test_seq_match(self):
        title1 = '''{FEETINGS:} Framework for Energy Efficiency Testing to Improve Environmental Goal of the Software'''
        title2 = '''{FEETINGS:} Framework for Energy Efficiency Testing to Improve eNvironmental Goals of the Software'''

        self.assertEqual(2, len(find_duplicates(add_mock_data(title1, title2))))

    def test_seq_match_2(self):
        title1 = '''Energy aware fuzzy approach for placement and consolidation in cloud data centers'''
        title2 = '''Energy Aware Fuzzy Approach for {VNF} Placement and Consolidation in Cloud Data Centers'''

        self.assertEqual(2, len(find_duplicates(add_mock_data(title1, title2))))

    def test_seq_match_3(self):
        title1 = '''A Novel Convolution Computing Paradigm Based on {NOR} Flash Array With High Computing Speed and Energy Efficiency'''
        title2 = '''A Novel Convolution Computing Paradigm Based on {NOR} Flash Array with High Computing Speed and Energy Efficient'''

        self.assertEqual(2, len(find_duplicates(add_mock_data(title1, title2))))

if __name__=='__main__':
	unittest.main()