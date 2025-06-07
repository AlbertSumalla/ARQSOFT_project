from abc import ABC, abstractmethod
from typing import List, Union
from entities.functions.Argument import Argument

# Definimos un alias para tipos numéricos
Number = Union[int, float]

class Function(Argument, ABC):

    def __init__(self) -> None:
        # Almacena el último resultado calculado
        self.result: Number = 0

    @abstractmethod
    def compute_formula(self, arguments: List[Argument]) -> Number:
       
        ...

    def get_value(self) -> Number:
        
        return self.result
