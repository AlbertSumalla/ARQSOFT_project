from entities.core.Cell import Cell
from entities.core.Coordinate import Coordinate
from entities.core.CellRange import CellRange
from entities.exceptions.Exceptions import BadCoordinateException
from entities.functions.NumericValue import NumericValue


class Spreadsheet:
    def __init__(self):
        self.cells: dict[Coordinate, Cell] = {}
        from entities.Factory.SpreadsheetFactory import SpreadsheetFactory
        self.factory = SpreadsheetFactory

    def set_cell(self, coord: Coordinate, cell: Cell) -> None:
        self.cells[coord] = cell # afegim cell unilateralment a la posicio de Coord, estigui o no.

        col_num_id = Coordinate.column_to_number(coord.column_id)  # posicio columna pero en numero      
        for col in range(1,col_num_id): # Recursivament busquem cells de 1 a col_num_cells i creem cel·les buides si no existeixen
            new_coord = self.factory.create_coordinate(self,Coordinate.number_to_column(col),coord.row_id)
            blank_cell = self.factory.create_cell(self,new_coord,"")
            if new_coord not in self.cells:
                self.cells[new_coord] = blank_cell


    def get_cell(self, coord: Coordinate) -> Cell:
        try:
            return self.cells.get(coord)
        except Exception:
            return None

    def get_cells_in_range(self, cell_range: CellRange) -> list[Cell | NumericValue]:
        start: Coordinate = cell_range.get_start()
        end: Coordinate = cell_range.get_end()

        start_col_idx = Coordinate.column_to_number(start.column_id)
        end_col_idx   = Coordinate.column_to_number(end.column_id)

        range_cell_list: list[Cell | NumericValue] = []
        # Recorrer cada fila y cada columna numérica
        for row in range(start.row_id, end.row_id + 1):
            for col_idx in range(start_col_idx, end_col_idx + 1):
                # Convertir índice de columna de vuelta a letras
                col_letters = Coordinate.number_to_column(col_idx)
                coord = Coordinate(col_letters, row)
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