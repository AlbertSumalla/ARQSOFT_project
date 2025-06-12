import re
from typing import List
from entities.exceptions.Exceptions import FormulaSyntaxError

class FormulaParser:
    VALID_FUNCTIONS = {"SUM", "MEAN", "MIN", "MAX"}
    VALID_OPERATORS = {"+", "-", "*", "/", "^"}

    @staticmethod
    def parse(tokens: List[str]) -> None:
        if not tokens:
            raise FormulaSyntaxError("Empty formula.")

        open_paren = 0
        prev = None  # one of: 'operand','operator','function','paren_open','comma'

        for i, tok in enumerate(tokens):
            ttype = FormulaParser.get_type(tok)

            if ttype == 'function':
                # must be followed by '('
                if i+1>=len(tokens) or tokens[i+1] != '(':
                    raise FormulaSyntaxError(f"Function '{tok}' missing '('.")
            elif tok == '(':
                open_paren += 1
                curr = 'paren_open'
            elif tok == ')':
                open_paren -= 1
                if open_paren < 0:
                    raise FormulaSyntaxError("Too many closing parentheses.")
                curr = 'paren_close'
            elif ttype == 'operator':
                # cannot start, follow operator, paren_open, or comma, or end
                if prev in (None, 'operator', 'paren_open', 'comma'):
                    raise FormulaSyntaxError(f"Operator '{tok}' misused.")
                if i == len(tokens)-1:
                    raise FormulaSyntaxError("Formula ends with operator.")
                curr = 'operator'
            elif tok == ',':
                # comma separates function args inside parens
                if prev in (None, 'operator', 'paren_open', 'comma'):
                    raise FormulaSyntaxError("Misplaced comma.")
                curr = 'comma'
            elif ttype in ('number','reference','range'):
                curr = 'operand'
            else:
                raise FormulaSyntaxError(f"Invalid token '{tok}'.")

            prev = curr

        if open_paren != 0:
            raise FormulaSyntaxError("Unbalanced parentheses.")

    @staticmethod
    def get_type(tok: str) -> str:
        if tok.upper() in FormulaParser.VALID_FUNCTIONS:
            return 'function'
        if tok in FormulaParser.VALID_OPERATORS:
            return 'operator'
        if re.fullmatch(r"\d+\.\d+|\d+", tok):
            return 'number'
        if re.fullmatch(r"[A-Za-z]+\d+:[A-Za-z]+\d+", tok):
            return 'range'
        if re.fullmatch(r"[A-Za-z]+\d+", tok):
            return 'reference'
        if tok in ('(', ')', ','):
            return tok
        return 'invalid'