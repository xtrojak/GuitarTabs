import unittest

from app.libs.parsing import Parser

TRACK = """4/3.0/6 - 0/3.3/6 - 2/3.0/5 #?
12/1 12/2 10/1 8/1 8/2 7/1 5/1 5/2 #! Part 1
8/1 7/1 5/2 7/1 5/1 5/2 3/1 1/1
1/2 3/1 5/1 3/2 3/1 0/1.0/2.0/6 #?

4/3.0/6 - 0/3.3/6 - 2/3.0/5 #?
12/1 12/2 10/1 8/1 8/2 7/1 5/1 5/2 #! Part 1
8/1 7/1 5/2 7/1 5/1 5/2 3/1 1/1
1/2 3/1 5/1 3/2 3/1 0/1.0/2.0/6 #?
"""

MINI_TRACK = """4/3.0/6 - 0/3.3/6 # small comment
12/1 12/2 10/1

8/1 7/1 5/2 7/1 5/1 5/2 3/1 1/1
"""


class ParsingTestCases(unittest.TestCase):
    def setUp(self):
        self.parser = Parser()

    def test_correct_tabs(self):
        track = open("Tracks/track01.tab", "r")
        result = self.parser.parse(track.read())
        self.assertTrue(result.success)

    def test_small_tabs(self):
        result = self.parser.parse(TRACK)
        self.assertTrue(result.success)

    def test_PostProcessor(self):
        result = self.parser.parse(TRACK)
        self.assertTrue(result.success)

        result = self.parser.transform(result.data)
        self.assertTrue(result.success)
