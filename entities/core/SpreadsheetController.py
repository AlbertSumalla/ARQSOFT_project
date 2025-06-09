from ..core.Spreadsheet import Spreadsheet
from ..core.Cell import Cell
from entities.content.NumericContent import NumericContent
from entities.content.TextContent import TextContent
from ..content.Formula import Formula
from entities.Factory.SpreadsheetFactory import SpreadsheetFactory
from exceptions.Exceptions import *

class SpreadsheetController:
    """
    Controlador principal de la hoja de cálculo. Expone métodos que el marker y la UI utilizan.
    """
    def __init__(self):
        # Inicializa la hoja usando la factoría para futuras extensiones
        self.spreadsheet: Spreadsheet = SpreadsheetFactory.create_spreadsheet()

    def set_cell_content(self, coord: str, str_content: str) -> None:
        """
        Modifica el contenido de la celda en la coordenada dada.
        """
        # Identificar tipo de entrada
        ctype = self.identify_input_type(str_content)
        if ctype == 'formula':
            expr = str_content[1:]
            content_obj = Formula(expr)
        elif ctype == 'numeric':
            try:
                num = float(str_content)
            except ValueError:
                raise EvaluationError(f"No se pudo convertir '{str_content}' a número")
            content_obj = NumericContent(num)
        else:
            content_obj = TextContent(str_content)
        try:
            self.spreadsheet.set_cell(coord, content_obj)
        except InvalidCellReferenceError:
            raise
        except CircularDependencyError:
            raise
        except Exception as e:
            raise EvaluationError(str(e))

    def get_cell_content_as_float(self, coord: str) -> float:
        """
        Devuelve el valor de la celda como flotante.
        """
        try:
            val = self.spreadsheet.get_cell_value(coord)
        except InvalidCellReferenceError:
            raise
        except Exception as e:
            raise EvaluationError(str(e))
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
        if isinstance(content, TextContent):
            return content.text
        try:
            val = self.get_cell_content_as_float(coord)
            return str(val)
        except EvaluationError:
            return str(content)

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
        Guarda la hoja en formato S2V en el path dado.
        """
        try:
            self.spreadsheet.save(file_path)
        except (PathError, S2VFormatError):
            raise
        except Exception as e:
            raise PathError(str(e))

    def load_spreadsheet_from_file(self, file_path: str) -> None:
        """
        Carga la hoja desde un archivo S2V.
        """
        try:
            self.spreadsheet.load(file_path)
        except (PathError, S2VFormatError):
            raise
        except Exception as e:
            raise S2VFormatError(str(e))

    @staticmethod
    def identify_input_type(input_string: str) -> str:
        """
        Identifica si el input es 'formula', 'numeric' o 'text'.
        """
        if input_string.startswith('='):
            return 'formula'
        try:
            float(input_string)
            return 'numeric'
        except ValueError:
            return 'text'

    @staticmethod
    def resolve_cell_references(spreadsheet: Spreadsheet, coordinate: str) -> None:
        """
        Propaga dependencias tras un cambio (Observer).
        """
        spreadsheet.recalculate_from(coordinate)

    @staticmethod
    def place_content_on_cell(cell_coordinate: str, content_object) -> None:
        """
        Asigna el objeto Content a la celda indicada.
        """
        raise NotImplementedError("Usar set_cell_content en lugar de place_content_on_cell")

    @staticmethod
    def close_spreadsheet(spreadsheet: Spreadsheet) -> None:
        """
        Cierra o limpia la hoja activa.
        """
        spreadsheet.clear()