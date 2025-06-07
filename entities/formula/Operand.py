from abc import ABC, abstractmethod

class Operand(ABC):
    def __init__(self, operator: str) -> None:
    self.operator: str = operator

    @abstractmethod
    def get_operand(self) -> object:
        pass
