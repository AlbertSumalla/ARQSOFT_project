from ..core.Cell import Cell
from entities.core.Coordinate import Coordinate
from entities.exceptions.Exceptions import InvalidCellReferenceError

class Spreadsheet:
    def __init__(self, rows: int, cols: int):
        self.cells: dict[Coordinate, Cell] = {}
        self.rows = rows
        self.cols = cols

    def set_cell(self, coord: Coordinate, cell: Cell) -> None:
        if coord not in self.cells:
            raise InvalidCellReferenceError(f"Cell {coord} does not exist")
        self.cells[coord] = cell

    def get_cell(self, coord: Coordinate) -> Cell:
        return self.cells[coord]
    
    def get_cell_value(self, coord: Coordinate) -> float:
        return self.get_cell(coord).get_cell_content()

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