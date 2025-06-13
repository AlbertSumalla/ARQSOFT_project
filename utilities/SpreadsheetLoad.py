# utilities/SpreadsheetLoad.py
import os
from Factory.SpreadsheetFactory import SpreadsheetFactory
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

        file = open(os.path.join(os.getcwd(),filepath), 'r')
        num_rows = 0
        while True:
            num_rows += 1
            line = file.readline().strip()
            line = line.replace(" ", "")
            row = line.split(";") #Aqui tengo un vector de (contenido) de celdas
            for i in row:
                letter = chr(ord('A') + num_rows)
                coord = f"{letter}{i}"
                self.controller.set_cell_content(coord, row[i])
            # if line is empty
            # end of file is reached
            if not line:
                break
        file.close()


    @staticmethod
    def int_to_string(col: int) -> str:
        """
        Convierte un índice de columna (1-based) a letra ('A', 'B', ...).
        """
        letters = 'ABCDEFGHIJKLMNOPQRSTUVWXYZ'
        if col < 1 or col > len(letters):
            raise ValueError(f"Índice de columna fuera de rango: {col}")
        return letters[col - 1]
