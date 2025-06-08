from ..core.Spreadsheet import Spreadsheet
from ..core.Cell import Cell
from ..content.NumericContent import NumericContent
from ..content.TextContent import TextContent
from ..content.Formula import Formula
from Factory.SpreadsheetFactory import SpreadsheetFactory
from exceptions.Exceptions import *
from ..core.ISpreadsheetControllerForChecker import ISpreadsheetFactoryForChecker
from core.Spreadsheet import Spreadsheet
from exceptions.Exceptions import *

class SpreadsheetController(ISpreadsheetFactoryForChecker):
    def __init__(self):
        self.spreadsheet = Spreadsheet()

    def set_cell_content(self, coord: str, str_content: str):
        # TODO: convertir str_content a Content y colocarlo
        pass

    def get_cell_content_as_float(self, coord: str) -> float:
        pass

    def get_cell_content_as_string(self, coord: str) -> str:
        pass

    def get_cell_formula_expression(self, coord: str) -> str:
        pass

    def save_spreadsheet_to_file(self, file_path: str):
        pass

    def load_spreadsheet_from_file(self, file_path: str):
        pass
