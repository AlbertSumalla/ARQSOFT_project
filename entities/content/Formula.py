from ..content.Content import Content
from ..formula.Tokenizer import Tokenizer
from ..formula.ShuntingYard import ShuntingYard
from ..formula.PostfixEvaluator import PostfixEvaluate
from ..formula.FormulaParse import FormulaParser
from ..exceptions.Exceptions import *


class Formula(Content):
    def __init__(self, formula_str: str, spreadsheet):
        self.formula_str = formula_str
        self.result = None
        self.spreadsheet = spreadsheet  # getter of spreadsheet instance

    def get_content(self) -> float:
        try:
            tokens_list = Tokenizer.tokenize(self.formula_str)
        except Exception as e:
            raise TokenizationError(f"Tokenization error: {e}")
        try:
            FormulaParser.parse(tokens_list)
        except Exception as e:
            raise FormulaSyntaxError(f"Syntax error: {e}")
        try:
            postfix_exp = ShuntingYard.generate_postfix_expression(tokens_list, self.spreadsheet)
        except Exception as e:
            raise PostfixGenerationError(f"Postfix generation error {e}")
        try:
            self.result = PostfixEvaluate.evaluate_postfix_expression(postfix_exp)
        except DivisionByZeroError as e:
            raise e
        except InvalidCellReferenceError as e:
            raise e
        except CircularDependencyError as e:
            raise e
        except Exception as e:
            raise EvaluationError(f"Evaluation formula error: {e}")

        return self.result