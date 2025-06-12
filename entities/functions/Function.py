# entities/formula/Function.py
from abc import ABC, abstractmethod
from typing import List
from entities.formula.Operand import Operand
from entities.exceptions.Exceptions import EvaluationError

class Function(Operand, ABC):
    def __init__(self,function_type, args: List[Operand]):
        self.args = args
        self.result = None
        self.type = function_type

    def compute_formula(self, values: List[float]) -> float:
        if self.type == 'SUM':
            return sum(values)
        pass

