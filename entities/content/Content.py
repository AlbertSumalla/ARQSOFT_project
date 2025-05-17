from abc import ABC, abstractmethod

class Content(ABC):
    @abstractmethod
    def evaluate(self) -> object:
        pass
