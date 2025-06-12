# entities/formula/Function.py
from abc import ABC, abstractmethod
from typing import List
from entities.formula.Operand import Operand
from entities.exceptions.Exceptions import EvaluationError

class Function(Operand, ABC):
    def __init__(self, args: List[Operand]):
        self.args = args

    def evaluate(self, sheet) -> float:
        """
        Evaluate all arguments, then compute the function-specific result.
        """
        try:
            values: List[float] = [arg.evaluate(sheet) for arg in self.args]
        except Exception as e:
            raise EvaluationError(f"Error evaluating function arguments: {e}")
        return self.compute(values)

    @abstractmethod
    def compute(self, values: List[float]) -> float:
        """
        Compute the function over the list of evaluated argument values.
        Must be implemented by concrete subclasses.
        """
        pass

class SumFunction(Function):
    def compute(self, values: List[float]) -> float:
        return sum(values)

class MinFunction(Function):
    def compute(self, values: List[float]) -> float:
        if not values:
            return 0.0
        return min(values)

class MaxFunction(Function):
    def compute(self, values: List[float]) -> float:
        if not values:
            return 0.0
        return max(values)

class MeanFunction(Function):
    def compute(self, values: List[float]) -> float:
        if not values:
            return 0.0
        return sum(values) / len(values)
