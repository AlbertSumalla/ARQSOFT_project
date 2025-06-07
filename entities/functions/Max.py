
from typing import List , Union
from Argument import Argument
from Function import Function
from NumericValue import NumericValue


# Definimos un alias para tipos numéricos
Number = Union[int, float]

class MAX(Function):
    def compute_formula(self, arguments: List[Argument]) -> Number:
        self.result = max(arg.get_value() for arg in arguments)
        return self.result