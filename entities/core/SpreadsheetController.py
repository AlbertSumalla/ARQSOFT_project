# entities/core/SpreadsheetController.py
from entities.core.Spreadsheet import Spreadsheet
from entities.core.Coordinate import Coordinate
from entities.content.NumericContent import NumericContent
from entities.content.TextContent import TextContent
from entities.content.Formula import Formula
from entities.Factory.SpreadsheetFactory import SpreadsheetFactory
from exceptions.Exceptions import *

class SpreadsheetController:
    def __init__(self):
        self.factory = SpreadsheetFactory()
        self.spreadsheet = None

    def create_spreadsheet(self, rows, cols) -> None:
        """
        1) Ask the factory for a blank sheet.
        2) For each position (r,c) build a Coordinate r,c
        3) Create a default empty TextContent via factory.create_text("")
        4) Wrap in a Cell and store in the sheet.
        """
        self.spreadsheet = self.factory.create_spreadsheet(rows, cols)

        for r in range(1, rows + 1):
            for c in range(1, cols + 1):
                letter = Coordinate.index_to_letter(c)
                coord = Coordinate.from_string(f"{letter}{r}")
                cell = self.factory.create_cell(coord, "")
                self.spreadsheet.set_cell(coord, cell)

    




    ##@brief Tries to set the content of a cell of the spreadsheet in a certain coordinate. See complete specification below following the link.
    #
    # @param coord   a string representing a coordinate in spreadsheet ('A10', for instance).
    #
    # @param str_content a string that contains the text representation of the purported new content ("=A1+10" or "2.0"
    # or "This is a string", for instance).
    #
    # @exception BadCoordinateException if the cellCoord argument does not represent a proper spreadsheet coordinate
    #
    # @exception ContentException if the content represents a formula which is not
    # correct by any other reason than introducing a circular dependency in the spreadsheet
    #
    # @exception CircularDependencyException if the code detects that the strContent is
    # formula that introduces in the spreadsheet some circular dependency

    def set_cell_content(self, coord, str_content):
        pass

    ##@brief Returns the value of the content of a cell as a float. See complete specification below following the link.
    #
    # @param coord   a string representing a coordinate in spreadsheet ('A10', for instance).
    #
    # @return a float representing the value of the content of a cell. If the cell contains a
    # textual content whose value is the textual representation of a number, it shall return this number. If the cell contains
    # a numerical content, it just returns its value. If the cell contentis a formula, it returns the number resulting
    # of evaluating such formula
    #
    # @exception BadCoordinateException if the cellCoord argument does not represent a proper spreadsheet coordinate
    #
    # @exception NoNumberException if the cell contains textual content whose value is a string that is not the textual
    # representation of a number

    def get_cell_content_as_float(self, coord):
        pass

    ##@brief Returns a string  version of the content of a cell.
    #
    # @param coord   a string representing a coordinate in spreadsheet ('A10', for instance).
    #
    # @return a string  version of the content of a cell. If the cell contains a
    # textual content it directly shall return its string value. If the cell contains a numerical content,
    # it returns the textual representation of the number . If the cell content is a formula, it returns the
    # string representing the number resulting of evaluating such formula
    #
    # @exception BadCoordinateException if the cellCoord argument does not represent a proper spreadsheet coordinate

    def get_cell_content_as_string(self, coord):
        pass

    ##@brief Returns the textual representation of the formula present in the cell whose coordiantes are represented by argument coord; the textual
    # representation of a formula MUST NOT INCLUDE THE '=' character, and there must not be any whitespace.
    #
    # @param coord   a string representing a coordinate in spreadsheet ('A10', for instance).
    #
    # @return a string containing the textual representation of a formula without the initial '=' character. Example "A1*B5*SUMA(A2:B27)"
    #
    # @exception BadCoordinateException if the coord argument does not represent a legal coordinate in the spreadsheet
    # OR if the coord argument represents a legal coordinate BUT cell in this coordinate DOES NOT CONTAIN A FORMULA

    def get_cell_formula_expression(self, coord):
        pass

    ##@brief Tries to save the spreadsheet into a file.
    #
    # @param s_name_in_user_dir  the local name of the file with respect to the folder where the invoking method is placed
    # (this is o because the markerrun shall look for files within the folder where testing classes are placed). The
    # absolute path shall be computed using the following expression: os.path.join(os.getcwd(),s_name_in_user_dir)
    #
    # @exception SavingSpreadSheetException if something has gone wrong while trying to write the spreadsheet into the aforementioned file

    def save_spreadsheet_to_file(self, s_name_in_user_dir):
        pass

    ##@brief Tries to load the spreadsheet from a file.
    #
    # @param s_name_in_user_dir  the local name of the file with respect to the folder where the invoking method is placed
    # (this is o because the markerrun shall look for files within the folder where testing classes are placed). The
    # absolute path shall be computed using the following expression: os.path.join(os.getcwd(),s_name_in_user_dir)
    #
    # @exception ReadingSpreadSheetException if something has gone wrong while trying to create spreadsheet and fill
    # it with the data present within the aforementioned file.

    def load_spreadsheet_from_file(self, s_name_in_user_dir):
        pass