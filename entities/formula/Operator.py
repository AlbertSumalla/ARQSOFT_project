class Operator:
    def __init__(self, symbol: str):
        self.symbol = symbol
        # Definimos precedencias y asociatividades por símbolo
        table = {
            '+': (2, 'left'),
            '-': (2, 'left'),
            '*': (3, 'left'),
            '/': (3, 'left'),
            '^': (4, 'right'),
        }
        if symbol not in table:
            raise ValueError(f"Operador desconocido: {symbol}")
        self.precedence, self.associativity = table[symbol]

    def apply(self, left_value: float, right_value: float) -> float:
        if self.symbol == '+':
            return left_value + right_value
        elif self.symbol == '-':
            return left_value - right_value
        elif self.symbol == '*':
            return left_value * right_value
        elif self.symbol == '/':
            if right_value == 0:
                raise ZeroDivisionError("División por cero en fórmula")
            return left_value / right_value
        elif self.symbol == '^':
            return left_value ** right_value
        

    def get_operator(self) -> str:
        return self.operator