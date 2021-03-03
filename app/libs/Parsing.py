from lark import Lark, Transformer, Tree, Token
from lark import UnexpectedCharacters, UnexpectedToken


class Result:
    """
    Class to represent output from the Parser.
    """
    def __init__(self, success, data):
        self.success = success
        self.data = data


GRAMMAR = r"""
    start: lines
    lines: line*
    line: selection+ COMMENT?
    selection: position selection | "-" selection | "-" | position
    position: tone "." position | tone
    tone : string "/" bar
    string : number
    bar : number
    
    COMMENT: "#" ("!" | "?")? /[^\n]/*
    
    number: INT
    %import common.INT
    %import common.WS
    %ignore WS
"""


class Parser:
    def __init__(self):
        self.parser = Lark(GRAMMAR, parser='lalr', propagate_positions=False, maybe_placeholders=False)

    # def parse(self, expression: str) -> Result:
    #     """
    #     Main method for parsing, first syntax_check is called which checks syntax and if it is
    #     correct, a parsed Tree is returned.
    #
    #     Then the tree is transformed using several Transformers in self.transform method.
    #
    #     :param expression: given string expression
    #     :return: Result containing parsed object or error specification
    #     """
    #     result = self.syntax_check(expression)
    #     if result.success:
    #         return self.transform(result.data)
    #     else:
    #         return result

    # def transform(self, tree: Tree) -> Result:
    #     """
    #     Apply several transformers to construct BCSL object from given tree.
    #
    #     :param tree: given parsed Tree
    #     :return: Result containing constructed BCSL object
    #     """
    #     try:
    #         complexer = ExtractComplexNames()
    #         tree = complexer.transform(tree)
    #         de_abstracter = TransformAbstractSyntax(complexer.complex_defns)
    #         tree = de_abstracter.transform(tree)
    #         tree = TreeToComplex().transform(tree)
    #         tree = TreeToObjects().transform(tree)
    #
    #         return Result(True, tree.children[0])
    #     except Exception as u:
    #         return Result(False, {"error": str(u)})

    def syntax_check(self, expression: str) -> Result:
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
