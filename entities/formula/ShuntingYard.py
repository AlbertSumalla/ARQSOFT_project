from typing import List

class ShuntingYard:
    """
    Implementación del algoritmo Shunting Yard para convertir expresiones infijas
'to notación postfija (postfix).
    """

    # Definimos precedencias y asociatividad de operadores
    _precedence = {
        '+': 2,
        '-': 2,
        '*': 3,
        '/': 3,
        '^': 4
    }
    # True = left-associative, False = right-associative
    _left_associative = {
        '+': True,
        '-': True,
        '*': True,
        '/': True,
        '^': False
    }

    @staticmethod
    def generate_postfix_expression(tokens: List[str]) -> List[str]:
        """
        Convierte una lista de tokens en notación postfix (RPN).

        :param tokens: lista de tokens infijos (p.ej. ['3', '+', '4', '*', '2', '/', '(', '1', '-', '5', ')', '^', '2', '^', '3'])
        :return: lista de tokens en postfix (p.ej. ['3', '4', '2', '*', '1', '5', '-', '2', '3', '^', '^', '/', '+'])
        """
        output_queue: List[str] = []
        operator_stack: List[str] = []

        for token in tokens:
            if token.isalnum() or token.replace('.', '', 1).isdigit():
                # Si es número o identificador, va directo a la salida
                output_queue.append(token)
            elif token in ShuntingYard._precedence:
                # Operador
                while operator_stack:
                    top = operator_stack[-1]
                    if top in ShuntingYard._precedence:
                        # Comparamos precedencia
                        if ((ShuntingYard._left_associative[token] and
                             ShuntingYard._precedence[token] <= ShuntingYard._precedence[top]) or
                            (not ShuntingYard._left_associative[token] and
                             ShuntingYard._precedence[token] < ShuntingYard._precedence[top])):
                            output_queue.append(operator_stack.pop())
                            continue
                    break
                operator_stack.append(token)
            elif token == '(':
                operator_stack.append(token)
            elif token == ')':
                # Sacamos hasta '('
                while operator_stack and operator_stack[-1] != '(':
                    output_queue.append(operator_stack.pop())
                # Descartamos '('
                if operator_stack and operator_stack[-1] == '(':  
                    operator_stack.pop()
                else:
                    raise ValueError("Paréntesis desbalanceados")
            else:
                # Token desconocido
                raise ValueError(f"Token no reconocido: {token}")

        # Al terminar, vaciamos la pila de operadores
        while operator_stack:
            top = operator_stack.pop()
            if top in ('(', ')'):
                raise ValueError("Paréntesis desbalanceados al final")
            output_queue.append(top)

        return output_queue