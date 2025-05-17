from Cell import Cell
from Coordinate import Coordinate

class Spreadsheet:
    def __init__(self, name="Untitled"):
        self.name = name
        self.cells = {}

    def get_cell(self, coord_str: str) -> Cell:
        return self.cells.get(coord_str)

    def set_cell(self, coord_str: str, content):
        coord = Coordinate.from_string(coord_str)
        self.cells[coord_str] = Cell(coord, content)
