# utilities/SpreadsheetSave.py

import os
from entities.exceptions.Exceptions import PathError

class SpreadsheetSave:

    @staticmethod
    def save_to_s2v(serial_rows, file_path: str) -> None:
        try:
            # Determine write mode: append if file exists and is not a directory, else write
            file_path = os.path.abspath(file_path)
            with open(file_path, 'w', encoding='utf-8') as f:
                for row in serial_rows:
                    # Write each cell followed by a semicolon
                    for i,cell in enumerate(row):
                        cell_str = str(SpreadsheetSave.smart_value(cell))
                        # si es fórmula, cambiamos ; internos por ,
                        if cell_str.startswith('='):
                            cell_str = cell_str.replace(';', ',')
                        f.write(cell_str)
                        if i < len(row)-1:
                            f.write(';')
                    # End of row
                    f.write('\n')
        except Exception as e:
            raise PathError(str(e))

    @staticmethod
    def smart_value(x):
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