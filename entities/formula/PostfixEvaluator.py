from typing import List, Union
from entities.formula.Operand import Operand
from entities.formula.Operator import Operator
from entities.exceptions.Exceptions import DivisionByZeroError
from entities.functions.NumericValue import NumericValue

Component = Union[Operand, NumericValue]

    ##
    # @brief Evaluates a postfix expression to extract its result.
    # @param postfix_exp: Postfix expression that has to be resolved.
    # @exception DivisionByZeroError Raised on division by zero.
    # @return Result: Float value after computing the evaluation.
class PostfixEvaluate:
    @staticmethod
    def evaluate_postfix_expression(postfix_exp: List[Component]) -> float:

        stack: List[float] = []
        for comp in postfix_exp:
            if isinstance(comp, NumericValue):
                # push operand's numeric value via get_value()
                stack.append(comp.getValue())
            elif isinstance(comp, Operator):
                # pop operands (right then left)
                right = stack.pop()
                left = stack.pop()
                try:
                    result = PostfixEvaluate.apply(comp, left, right)
                except ZeroDivisionError:
                    raise DivisionByZeroError("Division by zero during evaluation")
                stack.append(result)
            else:
                continue

        return stack[0] # Resultado final

    def apply(op: Operator, left: float, right: float) -> float:
        symbol = op.get_operator()
        if symbol == '+':
            return left + right
        elif symbol == '-':
            return left - right
        elif symbol == '*':
            return left * right
        elif symbol == '/':
            return left / right
        elif symbol == '^':
            return left ** right