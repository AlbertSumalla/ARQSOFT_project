from typing import List, Union
from entities.formula.Operand import Operand
from entities.formula.Operator import Operator
from entities.functions.Function import Function
from entities.core.Spreadsheet import Spreadsheet
from entities.Factory.FormulaFactory import FormulaFactory
from entities.exceptions.Exceptions import FormulaSyntaxError

Component = Union[Operand, Operator]

class ShuntingYard:
    def __init__(self):
        self.factory = FormulaFactory()
        from entities.core.SpreadsheetController import SpreadsheetController
        self.ctrl = SpreadsheetController()

    def generate_postfix_expression(self, tokens: List[str], spreadsheet: Spreadsheet) -> List[Component]:
        output_postfix: List[Component] = []
        op_stack: List[Union[str, Operator]] = []

        # Standard shunting-yard: handle numbers, cell refs, operators, functions, parentheses, argument separators
        for token in tokens:
            # 1) Operands: numbers or cell references
            if self.factory.is_numeric(token):
                num = self.factory.create_numeric(token)
                output_postfix.append(num)
            elif self.factory.is_cell_reference(token):
                val = self.ctrl.get_cell_content_as_float(token)
                output_postfix.append(self.factory.create_numeric(str(val)))

            # 2) Function names
            elif self.factory.is_function_name(token):
                op_stack.append(token)

            # 3) Argument separators (;
            #    Pop until left parenthesis is found
            elif token == ',' or token == ';':
                while op_stack and op_stack[-1] != '(':
                    output_postfix.append(op_stack.pop())

            # 4) Range operator ':' remains on stack, will be handled in function evaluation
            elif token == ':':
                op_stack.append(token)

            # 5) Left parenthesis always pushed
            elif token == '(':
                op_stack.append(token)

            # 6) Right parenthesis: pop until matching '('
            elif token == ')':
                # Pop operators to output until '('
                while op_stack and op_stack[-1] != '(':  
                    output_postfix.append(op_stack.pop())
                op_stack.pop()  # discard '('

                # After closing '(', if top is a function, pop it and compute immediately
                if op_stack and self.factory.is_function_name(op_stack[-1]):
                    func_name = op_stack.pop()

                    # Collect args from output_postfix by reconstructing from last function call
                    # We assume function args were already converted into numeric operands
                    # Here, extract the last N args until a marker or start; for simplicity, we
                    # re-run a simple scan: accumulate back until operator/function boundary
                    args: List[Operand] = []
                    while output_postfix and isinstance(output_postfix[-1], Operand):
                        args.append(output_postfix.pop())
                    args.reverse()

                    function: Function = self.factory.create_function(func_name)
                    result: Operand = function.compute_formula(args)
                    output_postfix.append(result)

            # 7) Operators
            elif self.factory.is_operator(token):
                op1: Operator = self.factory.create_operator(token)
                # While there is an operator at top with higher precedence (or equal for left-assoc)
                while op_stack and isinstance(op_stack[-1], Operator):
                    op2: Operator = op_stack[-1]
                    if (op1.associativity == 'left' and op1.precedence <= op2.precedence) or \
                       (op1.associativity == 'right' and op1.precedence < op2.precedence):
                        output_postfix.append(op_stack.pop())
                        continue
                    break
                op_stack.append(op1)

            else:
                raise FormulaSyntaxError(f"Unknown token '{token}'")

        # Pop any remaining operators
        while op_stack:
            top = op_stack.pop()
            if top == '(' or top == ')':
                raise FormulaSyntaxError("Mismatched parentheses in expression")
            output_postfix.append(top)

        return output_postfix
