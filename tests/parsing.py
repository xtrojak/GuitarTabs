import unittest

from app.libs.Parsing import Parser

TRACK = """4/3.0/6 - 0/3.3/6 - 2/3.0/5 #?
12/1 12/2 10/1 8/1 8/2 7/1 5/1 5/2 #! Part 1
8/1 7/1 5/2 7/1 5/1 5/2 3/1 1/1
1/2 3/1 5/1 3/2 3/1 0/1.0/2.0/6 #?

4/3.0/6 - 0/3.3/6 - 2/3.0/5 #?
12/1 12/2 10/1 8/1 8/2 7/1 5/1 5/2 #! Part 1
8/1 7/1 5/2 7/1 5/1 5/2 3/1 1/1
1/2 3/1 5/1 3/2 3/1 0/1.0/2.0/6 #?
"""


class ParsingTestCases(unittest.TestCase):
    def setUp(self):
        self.parser = Parser()

    def tearDown(self):
        pass

    def test_register_device(self):
        result = self.parser.syntax_check(TRACK)
        self.assertTrue(result.success)
