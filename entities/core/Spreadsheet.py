from ..core.Cell import Cell
from ..core.Coordinate import Coordinate
from Factory.SpreadsheetFactory import SpreadsheetFactory 

class Spreadsheet:
    def __init__(self, name="Untitled", factory=None):
        self.name = name
        self.cells = {}
        self.factory = factory

    def get_cell(self, coord_str: str) -> Cell:
        return self.cells.get(coord_str)

    def set_cell(self, coord_str: str, content):
        coord = Coordinate.from_string(coord_str)
        if self.factory:
            cell = self.factory.create_cell(coord, content)
        else:
            cell = Cell(coord, content)
        self.cells[coord_str] = cell
