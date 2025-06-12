from typing import List
from entities.functions.NumericValue import NumericValue
from entities.functions.Function import Function
from entities.core.CellRange import CellRange
from entities.core.Coordinate import Coordinate

class FormulaFactory:
    @staticmethod
    def create_function(name: str, args: List) -> Function:
        return Function(name, args)

    def create_numeric(value: str) -> NumericValue:
        return NumericValue(float(value))

    def create_cell_range(start: str, end: str) -> CellRange:
        return CellRange(start, end)


    @staticmethod
    def is_numeric(token: str) -> bool:
        try:
            float(token)
            return True
        except ValueError:
            return False

    @staticmethod
    def is_operator(token: str) -> bool:
        return token in ('+', '-', '*', '/')

    @staticmethod
    def is_cell_reference(token: str) -> bool:
        try:
            Coordinate.from_string(token)
            return True
        except Exception:
            return False

    @staticmethod
    def is_function_name(token: str) -> bool:
        return token.upper() in ('SUM', 'MIN', 'MAX', 'MEAN')