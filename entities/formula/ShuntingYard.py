# entities/formula/ShuntingYard.py
from typing import List, Union
from entities.formula.Operand import Operand
from entities.formula.Operator import Operator
from entities.functions.Function import Function
from entities.core.Spreadsheet import Spreadsheet
from entities.Factory.FormulaFactory import FormulaFactory
from entities.exceptions.Exceptions import FormulaSyntaxError
from entities.core.SpreadsheetController import SpreadsheetController

Component = Union[Operand,Operator]

class ShuntingYard:   
    def __init__(self):
        self.factory = FormulaFactory()
        self.ctrl = SpreadsheetController()

    def generate_postfix_expression(self, tokens: List[str], spreadsheet: Spreadsheet) -> List[Component]:
        output_postfix: List[Union[Operand,Operator]] = []
        op_stack: List[str | Operator] = []
        in_funct = False
        open_par = 0
        for token in tokens:

            if self.factory.is_function_name(token):
                in_funct = True
                op_stack.append(token)             
            
            elif token == ':':
                op_stack.append(token) 

            elif token == '(':
                op_stack.append(token)
                open_par += 1

            elif token == ')':
                open_par -= 1
                if open_par == 0:
                    in_funct = False
                # respectem sangria de cada funcio
                args: List[Union[str, Operand]] = []

                while op_stack and op_stack[-1] != '(':  # recolecta arguments
                    args.append(op_stack.pop())
                op_stack.pop()  # eliminar '('

                func_name = op_stack.pop()  # quitamos el nombre de la función
                args.reverse() # revertim ordre
                new_args = []
                for i,item in enumerate(args):
                    if item == ':':
                        cell_range = self.factory.create_cell_range(args[i-1], args[i+1])
                        list_cells = spreadsheet.get_cells_in_range(cell_range) # llista de celes en range
                        for element in list_cells: 
                            cell_content = self.ctrl.get_cell_content_as_float(element)
                            new_args.append(self.factory.create_numeric(str(cell_content)))
                i = 0
                while i < len(args): # borrar rango i appendear new_args
                    if args[i] == ':':
                        del args[i-1:i+2]
                        i = max(i-1, 0)
                    else:
                        i += 1
                for ele in new_args: # append NumericValues de range
                    args.append(ele)

                function = self.factory.create_function(func_name) 
                op_result = function.compute_formula(args) # numericValue
                args.clear() # netejar args
                
                if in_funct == False:
                    output_postfix.append(op_result) 
                    op_stack.clear()
                else:
                    op_stack.append(op_result)
                continue
                    
            elif self.factory.is_operator(token): # if its an operator
                output_postfix.append(self.factory.create_operator(token)) # append an Operator

            elif self.factory.is_numeric(token): # if its a number
                num = self.factory.create_numeric(token)
                if in_funct == False:
                    output_postfix.append(num)  # append an operand NumericValue
                else:
                    op_stack.append(num)  # append an operand NumericValue to the stack for function processing

            elif self.factory.is_cell_reference(token): # if its a cell reference (diferenciem rango i cell ref)
                if in_funct == False:
                    cell_content = self.ctrl.get_cell_content_as_float(token) # !!!! 
                    output_postfix.append(self.factory.create_numeric(str(cell_content)))  # append an operand NumericValue
                else:
                    cell_content = self.ctrl.get_cell_content_as_float(token) # !!!! no se si aixo funcionara
                    op_stack.append(self.factory.create_numeric(str(cell_content)))  # append an operand NumericValue
        while op_stack:
            op_stack.pop()
        return output_postfix                     
    
    
   