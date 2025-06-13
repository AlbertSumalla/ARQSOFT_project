# entities/formula/Function.py
from abc import ABC
from typing import List
from entities.formula.Operand import Operand
from entities.functions.Argument import Argument
from entities.functions.NumericValue import NumericValue

class Function(Operand, ABC):
    def __init__(self, function_type: str):
        self.type = function_type

    def compute_formula(self, args: List[Argument]) -> NumericValue:
        # imports locales para evitar circularidad
        if self.type == 'SUM':
            from entities.functions.Sum import SUM
            return SUM.compute_formula(args)
        elif self.type == 'MAX':
            from entities.functions.Max import MAX
            return MAX.compute_formula(args)
        elif self.type == 'MIN':
            from entities.functions.Min import MIN
            return MIN.compute_formula(args)
        elif self.type == 'MEAN':
            from entities.functions.Mean import MEAN
            return MEAN.compute_formula(args)