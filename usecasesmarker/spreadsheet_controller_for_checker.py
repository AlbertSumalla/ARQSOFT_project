# usecasesmarker/spreadsheet_controller_for_checker.py

import os

# Importaciones absolutas para evitar errores de paquete
from entities.core.SpreadsheetController import SpreadsheetController
from entities.bad_coordinate_exception import BadCoordinateException
from entities.content_exception import ContentException
from entities.circular_dependency_exception import CircularDependencyException
from entities.no_number_exception import NoNumberException
from usecasesmarker.saving_spreadsheet_exception import SavingSpreadSheetException
from usecasesmarker.reading_spreadsheet_exception import ReadingSpreadSheetException

class ISpreadsheetControllerForChecker:
    """
    Implementa la interfaz que el marker invoca.
    Cada método delega en tu SpreadsheetController y traduce
    firmas y excepciones al contrato que exige el marcador.
    """

    def __init__(self):
        self._ctrl = SpreadsheetController()

    def set_cell_content(self, coord: str, str_content: str) -> None:
        try:
            self._ctrl.set_cell(coord, str_content)
        except BadCoordinateException:
            raise
        except CircularDependencyException:
            raise
        except Exception as e:
            # errores de sintaxis o semántica de fórmula
            raise ContentException(str(e))

    def get_cell_content_as_float(self, coord: str) -> float:
        try:
            return self._ctrl.get_cell_value(coord)
        except BadCoordinateException:
            raise
        except NoNumberException:
            raise
        except Exception as e:
            raise ContentException(str(e))

    def get_cell_content_as_string(self, coord: str) -> str:
        try:
            return self._ctrl.get_cell_as_string(coord)
        except BadCoordinateException:
            raise

    def get_cell_formula_expression(self, coord: str) -> str:
        try:
            return self._ctrl.get_formula(coord)
        except BadCoordinateException:
            raise
        except CircularDependencyException:
            # si al obtener fórmula detecta ciclo
            raise
        except Exception as e:
            # no había fórmula válida
            raise ContentException(str(e))

    def save_spreadsheet_to_file(self, s_name_in_user_dir: str) -> None:
        path = os.path.join(os.getcwd(), s_name_in_user_dir)
        try:
            self._ctrl.save(path)
        except Exception as e:
            # errores de guardado
            raise SavingSpreadSheetException(str(e))

    def load_spreadsheet_from_file(self, s_name_in_user_dir: str) -> None:
        path = os.path.join(os.getcwd(), s_name_in_user_dir)
        try:
            self._ctrl.load(path)
        except Exception as e:
            # errores de carga
            raise ReadingSpreadSheetException(str(e))