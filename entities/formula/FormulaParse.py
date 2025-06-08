import re
from ..exceptions.Exceptions import FormulaSyntaxError

class FormulaParser:
    VALID_FUNCTIONS = {"SUM", "MEAN", "MIN", "MAX"}
    VALID_OPERATORS = {"+", "-", "*", "/"}

    @staticmethod
    def parse(tokens: list[str]) -> None:
        if not tokens:
            raise FormulaSyntaxError("Empty formula.")

        open_parentheses = 0
        prev_type = None  # "operand", "operator", "function", "paren_open"

        for i, token in enumerate(tokens):
            token_type = FormulaParser.get_token_type(token)

            if token_type == "function":
                if i + 1 >= len(tokens) or tokens[i + 1] != "(":
                    raise FormulaSyntaxError(f"Function '{token}' must be followed by '('.")
            elif token == "(":
                open_parentheses += 1
            elif token == ")":
                open_parentheses -= 1
                if open_parentheses < 0:
                    raise FormulaSyntaxError("Too many closing parentheses.")
            elif token_type == "operator":
                if prev_type in {"operator", None, "paren_open"}:
                    raise FormulaSyntaxError(f"Operator '{token}' used incorrectly.")
                if i == len(tokens) - 1:
                    raise FormulaSyntaxError("Formula cannot end with an operator.")
            elif token_type in {"reference", "range"}:
                pass  # valid
            else:
                raise FormulaSyntaxError(f"Unrecognized or invalid token: '{token}'.")

            prev_type = FormulaParser._type_label(token, token_type)

        if open_parentheses != 0:
            raise FormulaSyntaxError("Unbalanced parentheses.")

    @staticmethod
    def get_token_type(token: str) -> str:
        if token in FormulaParser.VALID_FUNCTIONS:
            return "function"
        elif token in FormulaParser.VALID_OPERATORS:
            return "operator"
        elif re.match(r"^[A-Z]+\d+$", token):
            return "reference"
        elif re.match(r"^[A-Z]+\d+:[A-Z]+\d+$", token):
            return "range"
        elif token in {"(", ")"}:
            return token
        else:
            return "invalid"

    @staticmethod
    def _type_label(token: str, token_type: str) -> str:
        if token == "(":
            return "paren_open"
        elif token == ")":
            return "paren_close"
        return token_type
