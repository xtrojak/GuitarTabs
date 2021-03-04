from lark import Lark, Transformer, Tree, exceptions
from lark import UnexpectedCharacters, UnexpectedToken

from app.libs.utils import SizeException


class Result:
    """
    Class to represent output from the Parser.
    """
    def __init__(self, success, data):
        self.success = success
        self.data = data


GRAMMAR = r"""
    start: section*
    section: line+ "\n"
    line: accord+ comment? "\n"
    comment: COMMENT
    accord: position | SKIP
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


class SizeChecker(Transformer):
    """
    Creates actual Complexes in rates of the rules - there it is safe,
    order is not important. Does not apply to the rest of the rule!
    """
    def line(self, matches):
        if len(matches) > 10:
            raise SizeException("Too many tones.")
        return Tree("line", matches)

    def section(self, matches):
        if len(matches) > 4:
            raise SizeException("Too many bars.")
        return Tree("lines", matches)


class Parser:
    def __init__(self):
        self.parser = Lark(GRAMMAR, parser='lalr', propagate_positions=False, maybe_placeholders=False)

    def check_size(self, tree: Tree) -> Result:
        """
        Apply several transformers to construct BCSL object from given tree.

        :param tree: given parsed Tree
        :return: Result containing constructed BCSL object
        """
        try:
            checker = SizeChecker()
            tree = checker.transform(tree)
            return Result(True, tree)
        except exceptions.VisitError as u:
            return Result(False, str(u))

    def parse(self, expression: str) -> Result:
        """
        Main method for parsing, calls Lark.parse method and creates Result containing parsed
         object (according to designed 'start' in grammar) or dict with specified error in case
         the given expression cannot be parsed.

        :param expression: given string expression
        :return: Result containing parsed object or error specification
        """
        try:
            tree = self.parser.parse(expression)
        except UnexpectedCharacters as u:
            return Result(False, {"unexpected": expression[u.pos_in_stream],
                                  "expected": u.allowed,
                                  "line": u.line, "column": u.column})
        except UnexpectedToken as u:
            return Result(False, {"unexpected": str(u.token),
                                  "expected": u.expected,
                                  "line": u.line, "column": u.column})
        return Result(True, tree)
