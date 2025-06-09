# entities/core/SpreadsheetController.py
from entities.core.Spreadsheet import Spreadsheet
from entities.content.NumericContent import NumericContent
from entities.content.TextContent import TextContent
from entities.content.Formula import Formula
from entities.Factory.SpreadsheetFactory import SpreadsheetFactory
from exceptions.Exceptions import *

class SpreadsheetController:
    """
    Controlador principal de la hoja de cálculo.
    """
    def __init__(self):
        # Inicializa la hoja mediante la factoría por defecto
        self.spreadsheet: Spreadsheet = SpreadsheetFactory.create_spreadsheet()

    def set_cell_content(self, coord: str, str_content: str) -> None:
        """
        Inserta contenido en la celda especificada (texto, número o fórmula), recalcula
        y propaga dependencias.
        """
        ctype = self.identify_input_type(str_content)
        if ctype == 'FORMULA':
            expr = str_content.lstrip('=')
            content_obj = Formula(expr)
        elif ctype == 'NUM':
            try:
                num = float(str_content)
            except ValueError:
                raise EvaluationError(f"No se pudo convertir '{str_content}' a número")
            content_obj = NumericContent(num)
        else:  # TEXT o EXIT
            content_obj = TextContent(str_content)

        try:
            # Asigna el contenido
            self.spreadsheet.set_cell(coord, content_obj)
            # Si es valor numérico o fórmula, actualiza su valor en el modelo
            if ctype in ('FORMULA', 'NUM'):
                val = self.get_cell_content_as_float(coord)
                self.spreadsheet.set_cell_value(coord, val)
            # Propaga recálculo a dependientes
            self.resolve_cell_references(coord)
        except (InvalidCellReferenceError, CircularDependencyError):
            # Se lanza directamente para el marker
            raise
        except Exception as e:
            # Errores genéricos de fórmula o parsing
            raise EvaluationError(str(e))

    def get_cell_content_as_float(self, coord: str) -> float:
        try:
            val = self.spreadsheet.get_cell_value(coord)
        except InvalidCellReferenceError:
            raise
        if not isinstance(val, (int, float)):
            raise EvaluationError(f"Contenido de la celda '{coord}' no es numérico")
        return float(val)

    def get_cell_content_as_string(self, coord: str) -> str:
        """
        Devuelve la representación en cadena del contenido de la celda.
        """
        try:
            content = self.spreadsheet.get_cell(coord).content
        except InvalidCellReferenceError:
            raise
        # Si es texto, devuelve directamente
        if isinstance(content, TextContent):
            return content.text
        # En caso contrario, formatea el valor numérico
        return str(self.get_cell_content_as_float(coord))

    def get_cell_formula_expression(self, coord: str) -> str:
        """
        Devuelve la expresión de la fórmula (sin '='). Lanza EvaluationError si no hay fórmula.
        """
        try:
            content = self.spreadsheet.get_cell(coord).content
        except InvalidCellReferenceError:
            raise
        if not isinstance(content, Formula):
            raise EvaluationError(f"La celda '{coord}' no contiene una fórmula")
        return content.expression

    def save_spreadsheet_to_file(self, file_path: str) -> None:
        """
        Guarda la hoja en disco en formato S2V.
        """
        try:
            self.spreadsheet.save(file_path)
        except (PathError, S2VFormatError):
            raise
        except Exception as e:
            raise PathError(str(e))

    def load_spreadsheet_from_file(self, file_path: str) -> None:
        """
        Carga la hoja desde disco (S2V) y reemplaza el modelo actual.
        """
        # Recrea un nuevo spreadsheet antes de cargar
        self.spreadsheet = SpreadsheetFactory.create_spreadsheet()
        try:
            self.spreadsheet.load(file_path)
        except (PathError, S2VFormatError):
            raise
        except Exception as e:
            raise S2VFormatError(str(e))

    def resolve_cell_references(self, coord: str) -> None:
        """
        Propaga el recálculo a todas las celdas que dependen de la coordenada dada.
        """
        deps = self.spreadsheet.get_cell(coord).get_coords_of_dependent_cells()
        for d in deps:
            self.spreadsheet.recalculate_from(d)

    @staticmethod
    def identify_input_type(input_string: str) -> str:
        """
        Determina si la entrada es FORMULA, NUM, TEXT o EXIT.
        """
        s = input_string.strip()
        lower = s.lower()
        if lower in ('cancel', 'exit', 'break'):
            return 'EXIT'
        if s.startswith('='):
            return 'FORMULA'
        try:
            float(s)
            return 'NUM'
        except ValueError:
            return 'TEXT'

    def place_content_on_cell(self, coord: str, content_obj) -> None:
        """
        Método de conveniencia para asignar un objeto Content a una celda.
        """
        self.spreadsheet.set_cell(coord, content_obj)

    def close_spreadsheet(self) -> None:
        """
        Limpia o cierra la hoja activa.
        """
        self.spreadsheet.clear()
