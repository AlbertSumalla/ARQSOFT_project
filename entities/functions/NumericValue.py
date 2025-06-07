from ..formula.Operand import Operand
class NumericValue(Operand):
    def __init__(self, value: float):
        self.value = value

    def setValue(self, value):
        """Set the internal value by parsing a string."""
        self.value = value

    def getValue(self):
        """Return the numeric value"""
        return self.value

    