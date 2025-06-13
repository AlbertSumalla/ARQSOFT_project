from entities.core.SpreadsheetController import SpreadsheetController

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

        # Determina dimensiones
        num_rows = spreadsheet.get_last_row()
        last_col = spreadsheet.get_last_column()  # e.g. 'A', 'B', ..., 'Z'
        num_columns = ord(last_col) - ord('A') + 1
        col_labels = [chr(ord('A') + i) for i in range(num_columns)]

        # Recopila valores de cada celda como string
        data = {}
        for row in range(1, num_rows + 1):
            for col in col_labels:
                coord = f"{col}{row}"
                try:
                    val = self.ctrl.get_cell_content_as_float(coord)
                    cell_str = str(val)
                except Exception:
                    cell_str = ""
                data[(row, col)] = cell_str

        # Calcula anchos de columna y fila
        row_label_width = len(str(num_rows))
        col_widths = {
            col: max(len(col), max(len(data[(r, col)]) for r in range(1, num_rows + 1)))
            for col in col_labels
        }

        # Función auxiliar para línea separadora
        def separator():
            sep = '+' + '-' * (row_label_width + 2)
            for col in col_labels:
                sep += '+' + '-' * (col_widths[col] + 2)
            sep += '+'
            return sep

        # Construye salida
        output = separator() + "\n"
        # Fila de encabezados
        header = '| ' + ' ' * row_label_width + ' '
        for col in col_labels:
            header += '| ' + col.center(col_widths[col]) + ' '
        header += '|' + "\n"
        output += header
        output += separator() + "\n"

        # Filas de datos
        for row in range(1, num_rows + 1):
            row_str = '| ' + str(row).rjust(row_label_width) + ' '
            for col in col_labels:
                cell_str = data[(row, col)].rjust(col_widths[col])
                row_str += '| ' + cell_str + ' '
            row_str += '|' + "\n"
            output += row_str
            output += separator() + "\n"

        return output
