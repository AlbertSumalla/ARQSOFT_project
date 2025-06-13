# entities/core/SpreadsheetController.py
from entities.core.Spreadsheet import Spreadsheet
from entities.core.Coordinate import Coordinate
from entities.core.Cell import Cell
from entities.content.NumericContent import NumericContent
from entities.content.TextContent import TextContent
from entities.content.Formula import Formula
from entities.Factory.SpreadsheetFactory import SpreadsheetFactory
from entities.exceptions.Exceptions import *

class SpreadsheetController(Spreadsheet):
    def __init__(self):
        self.factory = SpreadsheetFactory()
        self.spreadsheet = None

    def create_spreadsheet(self, rows: int, cols:int) -> None:
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
        # tornada a revisar, no testeada
        try: #parse coord
            coord_obj = Coordinate.from_string(coord)
            cell = self.spreadsheet.get_cell(coord_obj)
        except Exception:
            raise BadCoordinateException(f"No cell on this coordinate: {coord}")

        #content type
        ctype = self.identify_input_type(str_content)
        if ctype == "FORMULA":
            formula = str_content[1:]
            content_obj = self.factory.create_formula(formula, self.spreadsheet)
        elif ctype == "NUM":
            try:
                num = float(str_content)
            except ValueError:
                raise EvaluationError(f"Cannot convert '{str_content}' to number")
            content_obj = self.factory.create_number(num)
        else: #text case
            content_obj = self.factory.create_text(str_content)
        
        # Evaluate if is a formula and save cell. if not, just save the content
        if ctype in ("FORMULA"): 
            result = content_obj.get_content(formula, self.spreadsheet) #float del result of evaluation
            cell = self.factory.create_cell(coord_obj, result)
            cell.store_result(cell, result)
        else: # Si no es formula, guardem el contingut a la cell directament
            cell = self.factory.create_cell(coord_obj, content_obj)

        self.spreadsheet.set_cell(coord_obj, cell) #Set content value

        # propagate dependencies, no implementat encara
        # self.spreadsheet.recalculate_from(coord_obj)


    @staticmethod
    def identify_input_type(input_string: str) -> str:
        s = str(input_string).strip()
        if s.startswith('='):
            return 'FORMULA'
        try:
            float(s)
            return 'NUM'
        except ValueError:
            pass
        return 'TEXT'
    
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
        # feta desde 0, crec q esta  bé, no testeada
        try:
            coord_obj = Coordinate.from_string(coord)
            cell = self.spreadsheet.get_cell(coord_obj)  
        except Exception:
            raise BadCoordinateException(f"No cell on this coordinate: {coord}")
        
        formula = cell.get_cell_formula()
        if  formula is not None:
            return cell.get_cell_content() #retornem el resultat de la formula
        else:
            cell_content = cell.get_cell_content()
            ctype = self.identify_input_type(cell_content) # comprovem si es Numeric o Text
            if ctype == "TEXT":
                try:
                    return float(str(cell_content)) # S'intenta extreure el valor numéric del text
                except ValueError:
                    raise NoNumberException(f"Cell content '{cell_content}' is not a number")
            elif ctype == "NUM":
                return float(cell_content) # Si es un numero, retornem directament el valor numéric

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
        # re-feta, esta  bé, no testeada
        try:
            coord_obj = Coordinate.from_string(coord)
            cell = self.spreadsheet.get_cell(coord_obj) 
        except Exception:
            raise BadCoordinateException(f"No cell on this coordinate: {coord}")
        cell_content = cell.get_cell_content()

        return str(cell_content)

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
        # feta desde 0, crec q esta  bé, no testeada
        coord_obj = Coordinate.from_string(coord)
        try:
            cell = self.spreadsheet.get_cell(coord_obj)  
        except Exception:
            raise BadCoordinateException(f"No cell on this coordinate: {coord}")
        
        formula = cell.get_cell_formula()
        if  formula is not None:
            return formula #retornem el resultat de la formula

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