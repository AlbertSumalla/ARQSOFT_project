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

        ##
    # @brief Resolves the value of a referenced cells.
    # @param Spreadsheet: The spreadsheet object containing cells.
    # @param coordinate: The cell reference that has changed
    # @return None
    def resolve_cell_references(spreadsheet,coordinate):
        pass

    ##
    # @brief Identifies the type of content entered by the user.
    # @param input_string The raw content from user.
    # @return content type as str, that can be: 'text', 'numeric', or 'formula'.
    def identify_input_type(input_string):
        pass

    ##
    # @brief Sets a content on a specified cell.
    # @param cell_coordinate: Target cell coordinate where to place content.
    # @param Content_object: The content object to place in the cell.
    # @param content A Content object to assign to the cell.
    # @return None.
    def place_content_on_cell(cell_coordinate, content_object):
        pass

    ##
    # @brief Closes the currently active spreadsheet.
    # @param Spreadsheet: The Spreadsheet object to close.
    # @return None.
    def close_spreadsheet(spreadsheet):
        pass
