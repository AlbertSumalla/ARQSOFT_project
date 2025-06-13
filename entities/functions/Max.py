from typing import List
from Argument import Argument
from Function import Function
from entities.formula.Operand import Operand
from NumericValue import NumericValue
from entities.Factory.FormulaFactory import FormulaFactory

import numpy as np


class MAX(Function):
    def compute_formula(arguments: List[Argument]) -> NumericValue:

        result = np.max([arg.get_value() for arg in arguments])
        result_num = FormulaFactory.create_numeric(str(result))
        return result_num