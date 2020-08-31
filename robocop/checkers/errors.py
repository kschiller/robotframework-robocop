"""
Errors checkers
"""
from robocop.checkers import VisitorChecker
from robocop.rules import RuleSeverity


def register(linter):
    linter.register_checker(ParsingErrorChecker(linter))


class ParsingErrorChecker(VisitorChecker):
    """ Checker that returns Robot Framework DataErrors as lint errors. """
    rules = {
        "0401": (
            "parsing-error",
            "Robot Framework syntax error: %s",
            RuleSeverity.ERROR
        )
    }

    def __init__(self, *args):
        self.parse_only_section_not_allowed = False
        super().__init__(*args)

    def visit_Error(self, node):  # noqa
        if self.parse_only_section_not_allowed and 'Resource file with' not in node.error:
            return
        self.report("parsing-error", node.error, node=node)
