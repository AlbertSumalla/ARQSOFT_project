from entities.core.SpreadsheetController import SpreadsheetController
from collections import defaultdict
from entities.core.Coordinate import Coordinate
from utilities.SpreadsheetSave import SpreadsheetSave

class SpreadsheetRenderer:
    def __init__(self):
        # Instancia un controlador para evaluar celdas
        self.ctrl = SpreadsheetController()

    def display_spreadsheet(self, spreadsheet) -> str:
        """
        Generate and return a string representation of the spreadsheet's current values,
        including column headers and row numbers in a formatted grid.

        :param spreadsheet: an instance of the Spreadsheet model
        :return: multi-line string representing the spreadsheet
        """
        # Enlaza el controlador con el modelo
        self.ctrl.spreadsheet = spreadsheet


        row_max_col = defaultdict(int)
        for coord in self.ctrl.spreadsheet.cells:
            col_idx = Coordinate.column_to_number(coord.column_id)
            row_max_col[coord.row_id] = max(row_max_col[coord.row_id], col_idx + 1)

        serialized = []

        # 2) Serializo Matriz
        for row in sorted(row_max_col):
            max_col = row_max_col[row] - 1
            row_list = []
            # de 0..max_col-1
            for c in range(max_col):
                letter = Coordinate.index_to_letter(c)
                cell_coord = Coordinate(letter, row)
                cell = self.ctrl.spreadsheet.get_cell(cell_coord)

                if cell is None:
                    row_list.append("")
                else:
                    formula = cell.get_cell_formula()
                    if formula is not None:
                        row_list.append(f"={formula}")
                    else:
                        val = cell.get_cell_content()
                        row_list.append(str(val) if val is not None else "")
            serialized.append(row_list)

        for row in serialized:
            parts = []
            for cell in row:
                cell_str = str(SpreadsheetSave.smart_value(cell))
                if cell_str.startswith('='):
                    cell_str = cell_str.replace(';', ',')
                parts.append(cell_str)
            print(";".join(parts) + ";")
