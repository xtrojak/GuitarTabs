from lark import Lark, Transformer, Tree, exceptions
from lark import UnexpectedCharacters, UnexpectedToken
from wtforms import ValidationError

from app.libs.utils import SizeException


class Result:
    def __init__(self, success, data):
        self.success = success
        self.data = data


class Data:
    def __init__(self, bars, comments, depth):
        self.bars = bars
        self.boundaries, self.texts = self.compute_annotations(comments)
        self.depth = depth

    def __str__(self):
        return str(self.__dict__)

    def compute_annotations(self, comments):
        boundaries, texts = [], []
        inside_boundary = False
        for comment in comments:
            if not comment:
                if inside_boundary:
                    boundaries.append(3)
                else:
                    boundaries.append(0)
                texts.append(None)
            elif comment[0] == "!":
                inside_boundary = True
                boundaries.append(1)
                texts.append(comment[1:])
            elif comment[0] == "?":
                inside_boundary = False
                boundaries.append(2)
                texts.append(comment[1:])
            else:
                if inside_boundary:
                    boundaries.append(3)
                    texts.append(comment)
                else:
                    boundaries.append(0)
                    texts.append(comment)
        return boundaries, texts


GRAMMAR = r"""
    start: section*
    section: line+ ("\n")?
    line: accord+ comment? ("\n")? | comment ("\n")?
    comment: COMMENT
    accord: position | skip
    skip: SKIP
    position: tone ("." tone)*
    tone : string "/" bar
    string : number
    bar : number
    
    COMMENT: "#" ("!" | "?")? /[^\n]/*
    SKIP: "-"
    
    number: INT
    %import common.INT
    WS: /[ \t\f\r]/+
    %ignore WS
"""


class PostProcessor(Transformer):
    def __init__(self):
        super(PostProcessor, self).__init__()
        self.comments = []
        self.depth = 0

    def number(self, matches):
        return int(matches[0])

    def bar(self, matches):
        return matches[0]

    def string(self, matches):
        return matches[0]

    def tone(self, matches):
        return tuple(matches)

    def position(self, matches):
        return matches

    def skip(self, matches):
        return [(None, None)]

    def accord(self, matches):
        return matches[0]

    def comment(self, matches):
        return str(matches[0])[1:]

    def line(self, matches):
        if type(matches[-1]) == str:
            return {'tones': matches[:-1], 'comment': matches[-1]}
        else:
            return {'tones': matches, 'comment': None}

    def section(self, matches):
        bars = [match['tones'] for match in matches]
        comments = [match['comment'] for match in matches]
        return {'bars': bars, 'comments': comments}

    def start(self, matches):
        return Data([match['bars'] for match in matches],
                    sum([match['comments'] for match in matches], []),
                    len(matches))


class SizeChecker(Transformer):
    def line(self, matches):
        if len(matches) > 10:
            raise SizeException("Too many tones in one bar (the maximum is 10).")
        return Tree("line", matches)

    def section(self, matches):
        if len(matches) > 4:
            raise SizeException("Too many bars in one line (the maximum is 4).")
        return Tree("section", matches)


class Parser:
    def __init__(self):
        self.parser = Lark(GRAMMAR, parser='lalr', propagate_positions=False, maybe_placeholders=False)

    def transform(self, tree: Tree) -> Result:
        try:
            processor = PostProcessor()
            result = processor.transform(tree)
            return Result(True, result)
        except Exception as e:
            return Result(False, str(e))

    def check_size(self, tree: Tree) -> Result:
        try:
            checker = SizeChecker()
            tree = checker.transform(tree)
            return Result(True, tree)
        except exceptions.VisitError as u:
            return Result(False, str(u))

    def parse(self, expression: str) -> Result:
        try:
            tree = self.parser.parse(expression.rstrip())
        except UnexpectedCharacters as u:
            return Result(False, {"unexpected": expression[u.pos_in_stream],
                                  "expected": u.allowed,
                                  "line": u.line, "column": u.column})
        except UnexpectedToken as u:
            return Result(False, {"unexpected": str(u.token),
                                  "expected": u.expected,
                                  "line": u.line, "column": u.column})
        return Result(True, tree)


def validate_syntax(text):
    result = parser.parse(text)
    if not result.success:
        raise ValidationError(result.data)
    result = parser.check_size(result.data)
    if not result.success:
        raise ValidationError(result.data)
    return result.data


parser = Parser()
