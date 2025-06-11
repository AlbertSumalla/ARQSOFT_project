# usecasesmarker/spreadsheet_controller_for_checker.py

import os
from entities.core.SpreadsheetController import SpreadsheetController
from entities.exceptions.Exceptions import *
from usecasesmarker.saving_spreadsheet_exception import SavingSpreadsheetException
from usecasesmarker.reading_spreadsheet_exception import ReadingSpreadsheetException

class ISpreadsheetControllerForChecker:
    pass

class SpreadsheetControllerForChecker(ISpreadsheetControllerForChecker):
    def __init__(self):
        self._ctrl = SpreadsheetController()

    def set_cell_content(self, coord, str_content):
        try:
            self._ctrl.create_spreadsheet(rows=10, cols=10)
            print("Spreadsheet created successfully.")
        except Exception as e:
            raise ContentException("Error creating spreadsheet: " + str(e))
        try:
            self._ctrl.set_cell_content(coord, str_content)
        except InvalidCellReferenceError:
            raise BadCoordinateException()
        except CircularDependencyError:
            raise CircularDependencyException()
        except Exception as e:
            raise ContentException(str(e))

    def get_cell_content_as_float(self, coord):
        try:
            return self._ctrl.get_cell_content_as_float(coord)
        except InvalidCellReferenceError:
            raise BadCoordinateException()
        except NoNumberException:
            raise
        except Exception as e:
            raise ContentException(str(e))

    def get_cell_content_as_string(self, coord):
        try:
            return self._ctrl.get_cell_content_as_string(coord)
        except InvalidCellReferenceError:
            raise BadCoordinateException()

    def get_cell_formula_expression(self, coord):
        try:
            return self._ctrl.get_cell_formula_expression(coord)
        except InvalidCellReferenceError:
            raise BadCoordinateException()
        except ContentException:
            raise
        except Exception as e:
            raise ContentException(str(e))

    def save_spreadsheet_to_file(self, s_name_in_user_dir):
        path = os.path.join(os.getcwd(), s_name_in_user_dir)
        try:
            self._ctrl.save_spreadsheet_to_file(path)
        except Exception as e:
            raise SavingSpreadsheetException(str(e))

    def load_spreadsheet_from_file(self, s_name_in_user_dir):
        path = os.path.join(os.getcwd(), s_name_in_user_dir)
        try:
            self._ctrl.load_spreadsheet_from_file(path)
        except Exception as e:
            raise ReadingSpreadsheetException(str(e))
