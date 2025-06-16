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
        try:
            if self.type == 'SUMA':
                from entities.functions.Sum import SUMA
                return SUMA.compute_formula(args)
            elif self.type == 'MAX':
                from entities.functions.Max import MAX
                return MAX.compute_formula(args)
            elif self.type == 'MIN':
                from entities.functions.Min import MIN
                return MIN.compute_formula(args)
            elif self.type == 'PROMEDIO':
                from entities.functions.Mean import PROMEDIO
                return PROMEDIO.compute_formula(args)
        except Exception:
             if not args:
                from entities.Factory.FormulaFactory import FormulaFactory
                return FormulaFactory.create_numeric(FormulaFactory(),0)
        
    def get_operand(self) -> float:
        return self.type
