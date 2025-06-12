from ..formula.Operand import Operand

class NumericValue(Operand):
    def __init__(self, value: float):
        self.value = value

    def getValue(self):
        return self.value

    