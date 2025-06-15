from typing import List
from entities.functions.Argument import Argument
from entities.functions.Function import Function
from entities.formula.Operand import Operand
from entities.functions.NumericValue import NumericValue
from entities.Factory.FormulaFactory import FormulaFactory
import numpy as np



class SUMA(Function):
    def compute_formula(arguments: List[NumericValue]) -> NumericValue:

        result = np.sum([arg.getValue() for arg in arguments])
        result_num = FormulaFactory.create_numeric(FormulaFactory(),str(result))
        return result_num