from entities.functions.Function import Function
from entities.MyNumber import MyNumber

class Max(Function):
    @staticmethod
    def getInstance():
        return Max()

    def calculate(self, arguments: list[MyNumber]) -> MyNumber:
        # Si no hay argumentos, devolvemos 0 (o lanza excepción si lo prefieres)
        if not arguments:
            return MyNumber(0.0)
        # Inicializamos result al primer valor
        result = arguments[0].getAsDouble()
        # Buscamos el máximo
        for arg in arguments:
            value = arg.getAsDouble()
            if value > result:
                result = value
        return MyNumber(result)