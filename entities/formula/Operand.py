from abc import ABC, abstractmethod

class Operand(ABC):
    @abstractmethod
    def get_operand(self) -> object:
        pass