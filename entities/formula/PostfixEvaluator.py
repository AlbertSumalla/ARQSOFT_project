from typing import List, Union
from entities.formula.Operand import Operand
from entities.formula.Operator import Operator
from entities.exceptions.Exceptions import DivisionByZeroError
from entities.functions.NumericValue import NumericValue
from entities.exceptions.Exceptions import DivisionByZeroError, FormulaSyntaxError


Component = Union[Operator, Operand, NumericValue]

class PostfixEvaluate:
    ##
    # @brief Evaluates a postfix expression to extract its result.
    # @param postfix_exp: Postfix expression that has to be resolved.
    # @exception DivisionByZeroError Raised on division by zero.
    # @return Result: Float value after computing the evaluation.
    @staticmethod
    def evaluate_postfix_expression(postfix_exp: List[Component]) -> float:
        stack: List[float] = []

        for comp in postfix_exp:
            if isinstance(comp, Operand):
                stack.append(comp.getValue())

            # Operador: desapilar dos operandos y aplicar
            elif isinstance(comp, Operator):
                if len(stack) < 2:
                    raise FormulaSyntaxError("Insufficient operands for operator")
                right = stack.pop()
                left  = stack.pop()
                try:
                    result = comp.apply(left, right)
                except ZeroDivisionError:
                    raise DivisionByZeroError("Division by zero durig evaluation")
                stack.append(result)

            else:
                # No debería suceder si ShuntingYard produce solo Operands y Operators
                raise FormulaSyntaxError(f"Unknown token: {comp}")

        if len(stack) != 1:
            raise FormulaSyntaxError("Expresión postfija inválida: pila final con múltiples valores")

        return stack[0]
