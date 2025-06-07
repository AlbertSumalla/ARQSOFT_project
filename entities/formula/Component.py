from abc import ABC, abstractmethod

class Component(ABC):
    @abstractmethod
    def get_component(self) -> object:
        pass