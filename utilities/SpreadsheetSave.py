# utilities/SpreadsheetSave.py

import os
from entities.exceptions.Exceptions import PathError

class SpreadsheetSave:
    """
    Responsible for saving spreadsheets in S2V (semicolon-separated values) format.
    """

    @staticmethod
    def save_to_s2v(serial_rows, file_path: str) -> None:
        """
        Save the provided serialized rows to a file in S2V format.

        :param serial_rows: iterable of rows, each a sequence of cell string values
        :param file_path: path where the S2V file will be saved
        :raises PathError: if the file cannot be written
        """
        try:
            # Determine write mode: append if file exists and is not a directory, else write
            mode = 'a' if os.path.exists(file_path) and not os.path.isdir(file_path) else 'w'
            with open(file_path, mode, encoding='utf-8') as f:
                for row in serial_rows:
                    # Write each cell followed by a semicolon
                    for cell in row:
                        cell_str = str(SpreadsheetSave.smart_value(cell))
                        # si es fórmula, cambiamos ; internos por ,
                        if cell_str.startswith('='):
                            cell_str = cell_str.replace(';', ',')
                        f.write(cell_str)
                        f.write(';')
                    # End of row
                    f.write('\n')
        except Exception as e:
            # Wrap any IO error in PathError
            raise PathError(str(e))

    @staticmethod
    def smart_value(x):
        # si ya es float, lo dejamos listo para chequear .is_integer()
        if isinstance(x, float):
            if x.is_integer():
                return int(x)
            return x

        # si es una cadena, intentamos convertirla a float
        if isinstance(x, str):
            try:
                num = float(x)
            except ValueError:
                # no es un número ("=SUMA(A1:A2)", "hola", etc.)
                return x
            else:
                # si tras parsear a float sale entero, devolvemos int
                if num.is_integer():
                    return int(num)
                return num

        # cualquier otro tipo (int, Decimal, etc.)
        return x