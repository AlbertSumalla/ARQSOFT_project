from ..core.Spreadsheet import Spreadsheet
from ..core.Cell import Cell
from ..content.NumericContent import NumericContent
from ..content.TextContent import TextContent
from ..content.Formula import Formula
from Factory.SpreadsheetFactory import SpreadsheetFactory
from exceptions.Exceptions import *

class SpreadsheetController:
    def __init__(self, factory_type="DEFAULT"):
        self.factory = SpreadsheetFactory.get_instance(factory_type)
        self.spreadsheet = self.factory.create_spreadsheet()

    def set_cell_from_string(self, coordinate: str, input_str: str):
        """Detects the content type, creates content, and sets it on the cell."""
        content_type = self.identify_input_type(input_str)
        content = self.factory.create_content_object(input_str, content_type)
        self.spreadsheet.set_cell(coordinate, content)

    def identify_input_type(self, input_string: str) -> str:
        """Simple type detection."""
        if input_string.startswith("="):
            return "formula"
        try:
            float(input_string)
            return "numeric"
        except ValueError:
            return "text"

    def get_active_spreadsheet(self) -> Spreadsheet:
        return self.spreadsheet

    def close_spreadsheet(self):
        self.spreadsheet = None

    def create_empty_spreadsheet(self, rows: int, cols: int):
        if rows <= 0 or cols <= 0:
            raise InvalidSizeError("Spreadsheet size must be positive.")
        self.spreadsheet = self.factory.create_spreadsheet(rows, cols)
