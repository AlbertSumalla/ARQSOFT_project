# entities/functions/Max.py
from typing import List
from entities.functions.Argument import Argument
from entities.functions.NumericValue import NumericValue
from entities.functions.Function import Function     # import para heredar
import numpy as np
from entities.Factory.FormulaFactory import FormulaFactory

class MAX(Function):
    def compute_formula(arguments: List[NumericValue]) -> NumericValue:

        result = np.max([arg.getValue() for arg in arguments])
        result_num = FormulaFactory.create_numeric(str(result))
        return result_num

