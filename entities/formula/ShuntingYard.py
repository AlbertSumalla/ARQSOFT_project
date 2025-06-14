from dbm import error
from typing import List, Union
from content.NumericContent import NumericContent
from entities.formula.Operand import Operand
from entities.formula.Operator import Operator
from entities.functions.Function import Function
from entities.core.Spreadsheet import Spreadsheet
from entities.Factory.FormulaFactory import FormulaFactory
from entities.exceptions.Exceptions import FormulaSyntaxError , InvalidCellReferenceError
from entities.core.Coordinate import Coordinate

Component = Union[Operand, Operator]

class ShuntingYard:
    def __init__(self):
        self.factory = FormulaFactory()
        from entities.core.SpreadsheetController import SpreadsheetController
        self.ctrl = SpreadsheetController()

    def generate_postfix_expression(self, tokens: List[str], spreadsheet: Spreadsheet) -> List[Component]:
        output_postfix: List[Component] = []
        op_stack: List[Union[str, Operator]] = []
        new_args: List[Operand] = []
        self.ctrl.spreadsheet = spreadsheet
        
        for token in tokens:
            # 1) Operands: números y referencias a celdas
            if self.factory.is_numeric(token):
                output_postfix.append(self.factory.create_numeric(token))
            elif self.factory.is_cell_reference(token):
                val = self.ctrl.get_cell_content_as_float(token)
                output_postfix.append(self.factory.create_numeric(str(val)))

            # 2) Nombres de función
            elif self.factory.is_function_name(token):
                op_stack.append(token)

            # 3) Separadores de argumentos
            elif token == ';':
                while op_stack and op_stack[-1] != '(':
                    output_postfix.append(op_stack.pop())

            # 4) Operador de rango
            elif ':' in token:
                # Es un rango: separar inicio y fin, crear rango i hacer get-referencias
                str_coord_start, str_coord_end = token.split(':', 1)
                coord_start = Coordinate.from_string(str_coord_start)
                coord_end = Coordinate.from_string(str_coord_end)
                cell_range = self.factory.create_cell_range(coord_start,coord_end)

                contained_cells = spreadsheet.get_cells_in_range(cell_range)
                for cell in contained_cells:
                    if cell is None:
                        cell_val = self.factory.create_numeric(str(0))
                    else:
                        cell_val = cell.content
                        if type(cell_val) == NumericContent:
                            new_args.append(self.factory.create_numeric(str(cell_val)))
                        else:
                            raise InvalidCellReferenceError(f"The cell contains an str:{cell_val}")
                
                for ele in new_args:
                    op_stack.append(ele)

            # 5) Paréntesis izquierdo
            elif token == '(':
                op_stack.append(token)

            # 6) Paréntesis derecho: fin de expresión o de llamada a función
            elif token == ')':
                # Desapilar hasta el último '('
                while op_stack and op_stack[-1] != '(':  
                    output_postfix.append(op_stack.pop())
                op_stack.pop()  # eliminar '('

                # Si lo previo es nombre de función, recoger argumentos y expandir rangos
                if op_stack and self.factory.is_function_name(op_stack[-1]):
                    func_name = op_stack.pop()
                    # Reconstruir lista de args (tokens y Operands)
                    args: List[Union[str, Operand]] = []
                    while output_postfix and isinstance(output_postfix[-1], (Operand)):
                        args.append(output_postfix.pop())
                    # También puede haber ':' en op_stack, así que incorporar
                    # Buscamos backwards en stack temporal si fuera necesario
                    args.reverse()
                    function: Function = self.factory.create_function(func_name)
                    result: Operand = function.compute_formula(args)
                    output_postfix.append(result)

            # 7) Operadores binarios
            elif self.factory.is_operator(token):
                op1: Operator = self.factory.create_operator(token)
                while op_stack and isinstance(op_stack[-1], Operator):
                    op2: Operator = op_stack[-1]
                    if (op1.associativity == 'left' and op1.precedence <= op2.precedence) or \
                       (op1.associativity == 'right' and op1.precedence < op2.precedence):
                        output_postfix.append(op_stack.pop())
                        continue
                    break
                op_stack.append(op1)

            else:
                raise FormulaSyntaxError(f"Token desconocido '{token}'")

        # Vaciar stack de operadores restantes
        while op_stack:
            top = op_stack.pop()
            if top in ('(',')'):
                raise FormulaSyntaxError("Paréntesis desajustados en expresión")
            output_postfix.append(top)

        return output_postfix
