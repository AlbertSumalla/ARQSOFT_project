from ..content.Content import Content
from ..formula.Tokenizer import Tokenizer
from ..formula.ShuntingYard import ShuntingYard
from ..formula.FormulaEvaluate import PostfixEvaluate
from ..exceptions.Exceptions import *


class Formula(Content):
    def __init__(self, formula_str: str, spreadsheet):
        if not formula_str.startswith('='):
            raise FormulaSyntaxError("Formula must start with '='")
        self.raw_formula = formula_str
        self.formula_str = formula_str[1:]  # errase '='
        self.value = None
        self.spreadsheet = spreadsheet  # getter of spreadsheet instance

    def get_content(self):
        try:
            tokens_list = Tokenizer.tokenize(self.formula_str)
        except Exception as e:
            raise TokenizationError(f"Tokenization error: {e}")
        try:
            postfix_exp = ShuntingYard.generate_postfix_expression(tokens_list)
        except Exception as e:
            raise PostfixGenerationError(f"Postfix generation error {e}")
        try:
            self.value = PostfixEvaluate.evaluate_postfix_expression(postfix_exp, self.spreadsheet)
        except DivisionByZeroError as e:
            raise e
        except InvalidCellReferenceError as e:
            raise e
        except CircularDependencyError as e:
            raise e
        except Exception as e:
            raise EvaluationError(f"Evaluation formula error: {e}")

        return self.value

    def __str__(self):
        return self.raw_formula
