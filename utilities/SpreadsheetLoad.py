# utilities/SpreadsheetLoad.py
import os

from entities.exceptions.Exceptions import PathError, S2VFormatError

class SpreadsheetLoad:
    """
    Carga una hoja de cálculo desde un archivo S2V (semicolon-separated values).
    """
    def __init__(self, controller):
        # controller debe exponer set_cell_content(coord: str, content: str)
        self.controller = controller

    def load_spreadsheet(self, filepath: str) -> None:
        """
        Lee el archivo línea por línea, separa por ';', e invoca
        controller.set_cell_content para cada celda no vacía.
        """
        if not os.path.exists(filepath):
            raise PathError(f"Archivo no encontrado: {filepath}")
        try:
            with open(filepath, 'r', encoding='utf-8') as f:
                row_number = 1
                for line in f:
                    # Eliminar salto de línea y dividir
                    row_content = line.rstrip('\n').split(';')
                    for col_index, cell_text in enumerate(row_content, start=1):
                        if cell_text != '':
                            coord = self.int_to_string(col_index) + str(row_number)
                            # Asigna el contenido, puede lanzar excepciones de sintaxis
                            self.controller.set_cell_content(coord, cell_text)
                    row_number += 1
        except PathError:
            raise
        except Exception as e:
            # Cualquier otro error en parsing indica formato inválido
            raise S2VFormatError(str(e))

    @staticmethod
    def int_to_string(col: int) -> str:
        """
        Convierte un índice de columna (1-based) a letra ('A', 'B', ...).
        """
        letters = 'ABCDEFGHIJKLMNOPQRSTUVWXYZ'
        if col < 1 or col > len(letters):
            raise ValueError(f"Índice de columna fuera de rango: {col}")
        return letters[col - 1]
