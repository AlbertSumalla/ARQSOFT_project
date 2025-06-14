# utilities/SpreadsheetLoad.py
import os
from Factory.SpreadsheetFactory import SpreadsheetFactory
from entities.exceptions.Exceptions import PathError, S2VFormatError
from entities.core.Coordinate import Coordinate

class SpreadsheetLoad:
    """
    Carga una hoja de cálculo desde un archivo S2V (semicolon-separated values).
    """
    def __init__(self, controller):
        # controller debe exponer set_cell_content(coord: str, content: str)
        self.controller = controller

    @staticmethod
    def read_file_as_matrix(filepath: str) -> list:
        matrix = []
        with open(os.path.join(os.getcwd(), filepath), 'r') as file:
            for line in file:
                line = line.strip().replace(" ", "")
                if not line:
                    break
                matrix.append(line.split(";"))
        return matrix

    @staticmethod
    def load_spreadsheet(controller, filepath: str) -> None:
        with open(os.path.join(os.getcwd(), filepath), 'r') as file:
            for row_index, line in enumerate(file):
                line = line.strip().replace(" ", "")
                if not line:
                    break
                row = line.split(";")
                for col_index, content in enumerate(row):
                    if content != "":
                        coord = Coordinate.index_to_letter(col_index) + str(row_index + 1)
                        controller.set_cell_content(coord, content)

    @staticmethod
    def int_to_string(col: int) -> str:
        """
        Convierte un índice de columna (1-based) a letra ('A', 'B', ...).
        """
        letters = 'ABCDEFGHIJKLMNOPQRSTUVWXYZ'
        if col < 1 or col > len(letters):
            raise ValueError(f"Índice de columna fuera de rango: {col}")
        return letters[col - 1]
