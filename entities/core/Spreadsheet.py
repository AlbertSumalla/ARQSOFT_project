from ..core.Cell import Cell
from entities.core.Coordinate import Coordinate
from entities.core.CellRange import CellRange
from entities.exceptions.Exceptions import InvalidCellReferenceError

class Spreadsheet:
    def __init__(self):
        self.cells: dict[Coordinate, Cell] = {}

    def get_cols(self) ->   int:
        return self.cols
    
    def get_rows(self) -> int:
        return self.rows

    def set_cell(self, coord: Coordinate, cell: Cell) -> None:
        self.cells[coord] = cell

    def get_cell(self, coord: Coordinate) -> Cell:
        return self.cells.get(coord)

    def get_cells_in_range(self, cell_range: CellRange) -> list[Cell]:
        start = cell_range.get_start()
        end   = cell_range.get_end()
        range_cell_list: list[Cell] = []

        for r in range(start.row, end.row + 1):
            for c in range(start.col, end.col + 1):
                letter = Coordinate.index_to_letter(c)
                coord  = Coordinate.from_string(f"{letter}{r}")
                # get_cell will raise if missing
                cell = self.get_cell(coord)
                range_cell_list.append(cell)

        return range_cell_list

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