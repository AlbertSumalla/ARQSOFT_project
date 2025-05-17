from ..core.Coordinate import Coordinate
from ..content.Content import Content

class Cell:
    def __init__(self, coordinate: Coordinate, content: Content):
        self.coordinate = coordinate
        self.content = content
        self.dependencies = set()

    def evaluate(self):
        return self.content.evaluate()
