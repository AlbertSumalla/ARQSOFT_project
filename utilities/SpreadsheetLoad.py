# utilities/SpreadsheetLoad.py
import os
import re

from entities.exceptions.Exceptions import PathError, S2VFormatError
from entities.core.Coordinate import Coordinate
from entities.exceptions.Exceptions import DivisionByZeroError
from entities.Factory.SpreadsheetFactory import SpreadsheetFactory
from entities.core.SpreadsheetController import SpreadsheetController

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
                    if content == "":
                        continue

                    coord = Coordinate.index_to_letter(col_index) + str(row_index + 1)

                    # 1) volvemos a punto y coma los args de las fórmulas
                    content_norm = content
                    if content_norm.startswith('='):
                    # 1) convierte todos los commas a semicolon (argumentos de fórmula)
                        content_norm = content_norm.replace(',', ';')
                    # 2) pero restaura la coma que va justo antes de cualquier llamada a función anidada
                    # busca ';' seguido de un nombre de función (letras) y '('
                        content_norm = re.sub(r';(?=[A-Za-z_][A-Za-z0-9_]*\()', ',', content_norm)

                    try:
                        # 2) intentamos la carga normal (que internamente evalúa)
                        controller.set_cell_content(coord, content_norm)

                    except DivisionByZeroError:
                        # 3) si da división por cero, guardo solo la fórmula (sin evaluar)
                        coord_obj = Coordinate.from_string(coord)
                        formula_str = content_norm[1:]  # sin el '=' inicial
                        # celda con valor dummy (0) y fórmula
                        cell = controller.factory.create_cell(coord_obj, 0.0)
                        cell.formula = formula_str
                        controller.spreadsheet.set_cell(coord_obj, cell)

    @staticmethod
    def int_to_string(col: int) -> str:
        """
        Convierte un índice de columna (1-based) a letra ('A', 'B', ...).
        """
        letters = 'ABCDEFGHIJKLMNOPQRSTUVWXYZ'
        if col < 1 or col > len(letters):
            raise ValueError(f"Índice de columna fuera de rango: {col}")
        return letters[col - 1]
