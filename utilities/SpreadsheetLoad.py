# utilities/SpreadsheetLoad.py
import os
import re
from entities.exceptions.Exceptions import PathError, S2VFormatError
from entities.core.Coordinate import Coordinate
from entities.exceptions.Exceptions import DivisionByZeroError
from entities.core.SpreadsheetController import SpreadsheetController

class SpreadsheetLoad:
    def __init__(self, controller):
        from entities.Factory.SpreadsheetFactory import SpreadsheetFactory
        self.controller = None
        self.factory = SpreadsheetFactory()



    @staticmethod
    def load_spreadsheet(controller: SpreadsheetController, serialized_rows):
        compute_last = []
        # Guardem totes les posicions de les rows a la llista
        for num_row,row in enumerate(serialized_rows):
            for num_col,str_content in enumerate(row):
                serialized_rows[num_row][num_col] = str_content.replace(',', ';')
                coord_letter = Coordinate.number_to_column(num_col+1)
                coord_str = f"{coord_letter}{num_row+1}"
                try:
                    controller.set_cell_content(coord_str,str_content)
                except Exception:
                    compute_last.append(coord_str)
        
        # Les que no s'han pogut guardar (per dependencies circulars o similar, es computen ara recursivament. LIFO, si una torna a fallar, es posa la ultima a computar)
        timeout = 0
        while compute_last:
            coord_str = compute_last[0]
            compute_last.remove(coord_str)
            col_letter = coord_str[0]
            row_number = int(coord_str[1:])

            num_col = Coordinate.column_to_number(col_letter) - 1
            num_row = row_number - 1
            str_content = serialized_rows[num_row][num_col]
            try:
                controller.set_cell_content(coord_str,str_content)

                print(controller.spreadsheet.cells[Coordinate(col_letter,row_number)].formula)
                timeout = 0
            except Exception:
                # LIFO
                if timeout > 1: # evita bucle infinit en cas que un append falli
                    compute_last.append(coord_str)
                    timeout = 0
                else:
                    timeout += 1

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


