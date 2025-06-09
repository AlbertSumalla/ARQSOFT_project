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

    ##
    # @brief Updates all cells that depend on a modified cell.
    # @param cell: The cell whose value was updated.
    # @exception CircularDependencyError Raised if a circular dependency is found.
    # @exception InvalidCellReferenceError Raised if a dependency is invalid.
    # @return None.
    def update_dependent_cells(cell):
        pass

    ##
    # @brief Updates all cells and dependencies after importing a file.
    # @param Spreadsheet: The spreadsheet instance to which cells have to be updated.
    # @return None.
    def update_cell_values(spreadsheet):
        pass

    ##
    # @brief Scans the spreadsheet to detect any circular dependencies among cells.
    # @param Spreadsheet: The spreadsheet instance.
    # @exception CircularDependencyError Raised if circular dependencies are found.
    # @return None
    def identify_circular_dependencies(spreadsheet):
        pass