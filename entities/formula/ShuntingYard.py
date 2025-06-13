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
        self.ctrl.spreadsheet = spreadsheet
        
        for token in tokens:
            # 1) Operands: números y referencias a celdas
            if self.factory.is_numeric(token):
                output_postfix.append(self.factory.create_numeric(token))
            elif self.factory.is_cell_reference(token):
                print(f"Token '{token}'")
                try:
                    val = self.ctrl.get_cell_content_as_float(token)
                except Exception:
                    val = 0.0
                output_postfix.append(self.factory.create_numeric(str(val)))

            # 2) Nombres de función
            elif self.factory.is_function_name(token):
                op_stack.append(token)

            # 3) Separadores de argumentos
            elif token in (',',';'):
                while op_stack and op_stack[-1] != '(':
                    output_postfix.append(op_stack.pop())

            # 4) Operador de rango
            elif token == ':':
                op_stack.append(token)

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

                    # Expandir rangos dentro de args
                    new_args: List[Operand] = []
                    # Recorremos args original para detectar ':'
                    for i, item in enumerate(args):
                        if item == ':':
                            start_ref = args[i-1]
                            end_ref = args[i+1]
                            cell_range = self.factory.create_cell_range(start_ref, end_ref)
                            cells = spreadsheet.get_cells_in_range(cell_range)
                            for cell in cells:
                                cell_val = self.ctrl.get_cell_content_as_float(cell)
                                new_args.append(self.factory.create_numeric(str(cell_val)))
                    # Limpiar tokens de rango de args y añadir valores expandidos
                    i = 0
                    while i < len(args):
                        if args[i] == ':':
                            del args[i-1:i+2]
                            i = max(i-1, 0)
                        else:
                            i += 1
                    # Insertar al final los nuevos Operands
                    args.extend(new_args)

                    # Crear y evaluar función con args expandidos
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
