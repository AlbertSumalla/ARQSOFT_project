from abc import ABC, abstractmethod

class Argument(ABC):
    @abstractmethod
    def get_content(self) -> object:
        pass
