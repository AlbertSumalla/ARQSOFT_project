# entities/formula/Function.py
from abc import ABC, abstractmethod
from typing import List
from entities.formula.Operand import Operand
from entities.exceptions.Exceptions import EvaluationError
from entities.functions.NumericValue import NumericValue
from entities.functions.Max import MAX
from entities.functions.Min import MIN
from entities.functions.Mean import MEAN
from entities.functions.Sum import SUM
from entities.functions.Argument import Argument


class Function(Operand, ABC):
    def __init__(self,function_type: str):
        self.type = function_type

    def compute_formula(self, args: List[Argument]) -> NumericValue:
        if self.type == 'SUM':
            return SUM.compute_formula(args)
        elif self.type == 'MAX':   
            return MAX.compute_formula(args)
        elif self.type == 'MIN':
            return MIN.compute_formula(args)
        elif self.type == 'MEAN':
            return MEAN.compute_formula(args)

