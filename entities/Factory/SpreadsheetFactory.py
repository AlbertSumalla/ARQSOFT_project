from entities.core.Spreadsheet import Spreadsheet
from entities.core.Cell import Cell
from entities.content.NumericContent import NumericContent
from entities.content.TextContent import TextContent
from entities.content.Formula import Formula
from entities.exceptions.Exceptions import InvalidFunctionError
from entities.core.Coordinate import Coordinate

class SpreadsheetFactory:
    def __init__(self):
        pass

    def create_spreadsheet(self) -> Spreadsheet:
        return Spreadsheet()
    
    def create_coordinate(self,col: str,row: str) -> Coordinate:
<<<<<<< Updated upstream
        return Coordinate(col,row)
=======
        return 
>>>>>>> Stashed changes

    def create_cell(self, coordinate, content) -> Cell:
        return Cell(coordinate, content)

    def create_number(self, value: float) -> NumericContent:
        return NumericContent(value)

    def create_text(self, value: str) -> TextContent:
        return TextContent(value)

    def create_formula(self, formula_str: str, spreadsheet=None) -> Formula:
        return Formula(formula_str, spreadsheet)
