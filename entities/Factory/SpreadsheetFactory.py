from entities.core.Spreadsheet import Spreadsheet
from entities.core.Cell import Cell
from entities.content.NumericContent import NumericContent
from entities.content.TextContent import TextContent
from entities.content.Formula import Formula
from ..exceptions.Exceptions import InvalidFunctionError

class SpreadsheetFactory:
    def __init__(self):
        pass

    def create_spreadsheet(self, rows=10, cols=10) -> Spreadsheet:
        return Spreadsheet(rows, cols)

    def create_cell(self, coordinate, content) -> Cell:
        return Cell(coordinate, content)

    def create_number(self, value: float) -> NumericContent:
        return NumericContent(value)

    def create_string(self, value: str) -> TextContent:
        return TextContent(value)

    def create_formula(self, formula_str: str, spreadsheet=None) -> Formula:
        return Formula(formula_str, spreadsheet)

    def create_content_object(self, input_str: str, content_type: str, spreadsheet=None):
        if content_type == "numeric":
            return self.create_number(float(input_str))
        elif content_type == "text":
            return self.create_string(input_str)
        elif content_type == "formula":
            return self.create_formula(input_str, spreadsheet)
        else:
            raise InvalidFunctionError(f"Unknown content type: {content_type}")
