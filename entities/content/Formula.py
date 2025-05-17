from ..content.Content import Content
from ..formula.Tokenizer import Tokenizer
from ..formula.ShuntingYard import ShuntingYard
from ..formula.PostfixGener import PostfixEvaluator
from ..exceptions.Exceptions import *


class Formula(Content):
    def __init__(self, formula_str: str, spreadsheet):
        if not formula_str.startswith('='):
            raise FormulaSyntaxError("Las fórmulas deben comenzar con '='")
        self.raw = formula_str
        self.formula_str = formula_str[1:]  # errase '='
        self.value = None
        self.spreadsheet = spreadsheet  # getter of spreadsheet

    def evaluate(self):
        try:
            tokens = Tokenizer.tokenize(self.formula_str)
        except Exception as e:
            raise TokenizationError(f"Error de tokenización: {e}")
        try:
            postfix = ShuntingYard.to_postfix(tokens)
        except Exception as e:
            raise PostfixGenerationError(f"Error al generar postfix: {e}")
        try:
            self.value = PostfixEvaluator.evaluate(postfix, self.spreadsheet)
        except DivisionByZeroError as e:
            raise e
        except InvalidCellReferenceError as e:
            raise e
        except CircularDependencyError as e:
            raise e
        except Exception as e:
            raise EvaluationError(f"Error al evaluar la fórmula: {e}")

        return self.value

    def get_as_string(self):
        return self.formula_str

    def __str__(self):
        return self.raw
