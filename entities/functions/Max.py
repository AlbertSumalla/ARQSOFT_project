from Function import Function
from NumericValue import NumericValue

class Max(Function):
    @staticmethod
    def getInstance():
        return Max()

    def calculate(self, arguments: list[NumericValue]) -> NumericValue:
        # Si no hay argumentos, devolvemos 0 (o lanza excepción si lo prefieres)
        if not arguments:
            return NumericValue(0.0)
        # Inicializamos result al primer valor
        result = arguments[0].getAsDouble()
        # Buscamos el máximo
        for arg in arguments:
            value = arg.getAsDouble()
            if value > result:
                result = value
        return NumericValue(result)