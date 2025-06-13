from entities.formula.Operand import Operand
from entities.functions.Argument import Argument

class NumericValue(Operand,Argument):
    def __init__(self, value: float):
        self.value = value

    def getValue(self):
        return self.value

    