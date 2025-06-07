from typing import List , Union
from Argument import Argument
from Function import Function
from NumericValue import NumericValue


# Definimos un alias para tipos numéricos
Number = Union[int, float]

class MEAN(Function):
    def compute_formula(self, arguments: List[Argument]) -> Number:
        total = sum(arg.get_value() for arg in arguments)
        count = len(arguments)
        self.result = total / count if count else 0
        return self.result