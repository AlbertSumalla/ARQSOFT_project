# entities/formula/ShuntingYard.py
from typing import List, Union
from entities.formula.Operand import Operand
from entities.formula.Operator import Operator
from entities.functions.Function import Function
from entities.Factory.FormulaFactory import FormulaFactory
from entities.exceptions.Exceptions import FormulaSyntaxError
from entities.core.SpreadsheetController import SpreadsheetController

Component = Union[Operand,Operator]

class ShuntingYard:   
    def __init__(self):
        self.factory = FormulaFactory()
        self.ctrl = SpreadsheetController()
               
    
    def generate_postfix_expression(self, tokens: List[str], spreadsheet) -> List[Component]:
        output_postfix: List[Union[Operand,Operator]] = []
        op_stack: List[str | Operator] = []
        in_funct = False
        
        for i, token in enumerate(tokens):
            next_token = tokens[i+1] if i+1 < len(tokens) else None # mirem el next token

            if self.factory.is_function_name(token):
                in_funct = True
                op_stack.append(token)             
            
            if in_funct == True: # si es una funcio
                if token == '(':
                    op_stack.append(token)
                    pass
                
            # dema entendre com gestionar op_stack i amb un while computar les funcions internes, crec que es lo millor.
            else:
                if self.factory.is_operator(token): # if its an operator
                    output_postfix.append(self.factory.create_operator(token)) # append an Operator

                elif self.factory.is_numeric(token): # if its a number
                    output_postfix.append(self.factory.create_numeric(token))  # append an operand NumericValue
                
                elif self.factory.is_cell_reference(token): # if its a cell reference
                    cell_content = self.ctrl.get_cell_content_as_float(token) # !!!! no se si aixo funcionara
                    output_postfix.append(self.factory.create_numeric(str(cell_content)))  # append an operand NumericValue

        
                
    def generate_postfix_expression(tokens: List[str], spreadsheet) -> List[Component]:
        output_queue: List[Component] = []
        op_stack: List[Union[str, Operator, Function]] = []

        for token in tokens:
            # Operand: number, reference, or range
            if ShuntingYard.is_numeric(token) or ShuntingYard.is_cell_reference(token) or ':' in token:
                comp = FormulaFactory.create_component(token, spreadsheet)
                output_queue.append(comp)

            # Function name
            elif FormulaFactory.is_function_name(token):
                # Push function identifier onto stack
                op_stack.append(token)

            # Argument separator (comma)
            elif token == ',':
                # Pop until left parenthesis
                while op_stack and op_stack[-1] != '(':  # type: ignore
                    output_queue.append(op_stack.pop())
                if not op_stack:
                    raise FormulaSyntaxError("Misplaced comma or mismatched parentheses.")

            # Left parenthesis
            elif token == '(':
                op_stack.append(token)

            # Right parenthesis
            elif token == ')':
                # Pop until matching left parenthesis
                while op_stack and op_stack[-1] != '(':  # type: ignore
                    output_queue.append(op_stack.pop())
                if not op_stack:
                    raise FormulaSyntaxError("Mismatched parentheses.")
                # Pop the '('
                op_stack.pop()
                # If top of stack is a function name, pop it to output
                if op_stack and isinstance(op_stack[-1], str) and FormulaFactory.is_function_name(op_stack[-1]):  # type: ignore
                    func_name = op_stack.pop()  # type: ignore
                    # The arguments must have been parsed earlier; build the Function now
                    # Retrieve argument Components from output_queue until matching marker
                    # (In a fuller implementation, you'd track function argument boundaries.)
                    # For simplicity, assume FunctionFactory builds with no args here.
                    func = FormulaFactory.create_function(func_name, [])
                    output_queue.append(func)

            # Operator
            elif FormulaFactory.is_operator(token):
                op1 = FormulaFactory.create_component(token)
                # Pop operators of greater or equal precedence
                while op_stack and isinstance(op_stack[-1], Operator):
                    op2 = op_stack[-1]  # type: ignore
                    if op1.precedence <= op2.precedence:
                        output_queue.append(op_stack.pop())
                    else:
                        break
                op_stack.append(op1)

            else:
                raise FormulaSyntaxError(f"Unrecognized token in ShuntingYard: {token}")

        # Drain the operator stack
        while op_stack:
            top = op_stack.pop()
            if top in ('(', ')'):
                raise FormulaSyntaxError("Mismatched parentheses in expression.")
            output_queue.append(top)  # type: ignore

        return output_queue
