# entities/core/SpreadsheetController.py
import os
from collections import deque
from typing import List
from collections import defaultdict
from entities.core.Spreadsheet import Spreadsheet
from entities.core.Coordinate import Coordinate
from entities.core.Cell import Cell
from entities.content.NumericContent import NumericContent
from entities.content.TextContent import TextContent
from entities.content.Formula import Formula
from entities.Factory.SpreadsheetFactory import SpreadsheetFactory
from entities.Factory.FormulaFactory import FormulaFactory
from entities.exceptions.Exceptions import *
from utilities.SpreadsheetSave import SpreadsheetSave
from usecasesmarker.saving_spreadsheet_exception import SavingSpreadsheetException
from entities.formula.Tokenizer import Tokenizer

class SpreadsheetController(Spreadsheet):
    def __init__(self):
        self.factory = SpreadsheetFactory()
        self.factory_formula = FormulaFactory()
        self.spreadsheet = None

    def create_spreadsheet(self) -> Spreadsheet:
        self.spreadsheet = self.factory.create_spreadsheet()
        return self.spreadsheet

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
        try: # parse
            coord_obj = Coordinate.from_string(coord)  
        except Exception:
            raise BadCoordinateException(f"Bad Coordinate format: {coord}")

        #content type
        ctype = self.identify_input_type(str_content)
        if ctype == "FORMULA":
            formula = str_content[1:]
            content_obj = self.factory.create_formula(formula, self.spreadsheet)
            #dependency , tokenizer,
        elif ctype == "NUM":
            try:
                num = float(str_content)
            except ValueError:
                raise EvaluationError(f"Cannot convert '{str_content}' to number")
            content_obj = self.factory.create_number(num)
        else: #text case
            content_obj = self.factory.create_text(str_content)
        
        # Evaluate if is a formula and save cell. if not, just save the content
        if ctype == "FORMULA":
            result = content_obj.get_content()  # float del result of evaluation
            cell = self.factory.create_cell(coord_obj, result)
            cell.formula = str_content
            self.set_dependencies(cell)
            #self.identify_circular_dependencies(cell)
        else: # Si no es formula, guardem el contingut a la cell directament
            cell = self.factory.create_cell(coord_obj, content_obj.get_content())

        self.spreadsheet.set_cell(coord_obj, cell) #Set content value
        
        self.update_dependent_cells(cell)

    def set_dependencies(self, cell: Cell):
        tokens = Tokenizer.tokenize(cell.formula[1:])
        dependencies: List[Coordinate] = []
        for token in tokens:
            # single-cell tokens
            try:
                dependencies.append(Coordinate.from_string(token))
            except Exception:
                pass
            # range tokens
            if ':' in token:
                start_str, end_str = token.split(':', 1)
                try:
                    start = Coordinate.from_string(start_str)
                    end = Coordinate.from_string(end_str)
                except Exception:
                    continue
                cell_range = self.factory_formula.create_cell_range(start, end)
                sc = cell_range.get_start()
                ec = cell_range.get_end()
                sc_idx = Coordinate.column_to_number(sc.column_id)
                ec_idx = Coordinate.column_to_number(ec.column_id)
                for r in range(sc.row_id, ec.row_id + 1):
                    for c_idx in range(sc_idx, ec_idx + 1):
                        col_letters = Coordinate.number_to_column(c_idx)
                        dependencies.append(Coordinate(col_letters, r))
        # detect circular dependencies before setting
        self.identify_circular_dependencies(cell)
        cell.set_cell_dependencies(dependencies)

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

    ##
    # @brief Updates all cells that depend on a modified cell.
    # @param cell: Cell containing the dependancies to be updated
    # @return None.
    def update_dependent_cells_err(self, cell:Cell):
        cell_dep = cell.dependencies
        while cell_dep:
            coord = cell_dep[0]
            cell_dep.remove(coord)
            str_coord = str(coord)
            cell_up = self.spreadsheet.cells[coord]
            formula = cell_up.formula

            if formula != None:
                for new_cord in cell_up.dependencies:
                    cell_dep.append(new_cord)
                if not formula.startswith('='):
                    formula = '=' + formula
                self.set_cell_content(str_coord,formula)

        for coord in cell_dep:
            str_coord = str(coord)
            str_content = self.spreadsheet.cells[coord].formula
            if str_content:
                if not str_content.startswith('='):
                    str_content = '=' + str_content
            
            self.set_cell_content(str_coord,str_content)

    def update_dependent_cells(self, changed_cell: Cell) -> None:

        start_coord = changed_cell.coordinate

        # queue and visitor
        queue = deque([start_coord])
        visited = {start_coord}

        while queue:
            curr = queue.popleft()
            for coord, cell in list(self.spreadsheet.cells.items()):
                # coord es un Coordinate, cell.dependencies es List[Coordinate]
                if curr in cell.dependencies and coord not in visited:
                    # 5) Reconstruir el contenido con '=' garantizado
                    formula = getattr(cell, 'formula', None)
                    if not formula: # no es una formula
                        continue
                    if not formula.startswith('='):
                        formula = '=' + formula

                    self.set_cell_content(str(coord), formula)
                    visited.add(coord)
                    queue.append(coord)


    ##
    # @brief Scans the spreadsheet to detect any circular dependencies among cells.
    # @param Spreadsheet: The spreadsheet instance.
    # @exception CircularDependencyError Raised if circular dependencies are found.
    # @return None
    def identify_circular_dependencies(self, cell: Cell):
        def has_path(src: Coordinate, dst: Coordinate, visited: set) -> bool:
            if src == dst:
                return True
            visited.add(src)
            existing = self.spreadsheet.cells.get(src)
            if not existing:
                return False
            for dep in existing.dependencies:
                if dep not in visited:
                    if has_path(dep, dst, visited):
                        return True
            return False
        for dep in cell.dependencies:
            if dep == cell.coordinate:
                raise CircularDependencyException(
                    f"Circular dependency detected: {cell.coordinate} refers to itself"
                )
            # if dep can reach cell, a cycle would form
            if has_path(dep, cell.coordinate, set()):
                raise CircularDependencyException(
                    f"Circular dependency detected between {cell.coordinate} and {dep}"
                )

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
        try:
            coord_obj = Coordinate.from_string(coord)
            cell = self.spreadsheet.get_cell(coord_obj)  
        except Exception:
            raise BadCoordinateException(f"Empty Cell: {coord}")
        if cell is None:
            return 0
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
                    if cell_content == "" or cell_content == None:
                        return 0
                    else:
                        raise NoNumberException(f"Cell '{cell_content}' has no number.")
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
        try:
            coord_obj = Coordinate.from_string(coord)
            cell = self.spreadsheet.get_cell(coord_obj) 
        except Exception:
            raise BadCoordinateException(f"Empty Cell: {coord}")
        if  cell is None:
            return ""
        else:
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
        coord_obj = Coordinate.from_string(coord)
        try:
            cell = self.spreadsheet.get_cell(coord_obj)  
        except Exception:
            raise BadCoordinateException(f"No cell on this coordinate: {coord}")
        try:
            formula = cell.get_cell_formula()
        except Exception:
            formula = None
        if  formula is not None:
            s = str(formula).strip()
            if s.startswith('='):
                return formula #retornem el resultat de la formula
            else:
                return "=" + formula

    ##@brief Tries to save the spreadsheet into a file.
    #
    # @param s_name_in_user_dir  the local name of the file with respect to the folder where the invoking method is placed
    # (this is o because the markerrun shall look for files within the folder where testing classes are placed). The
    # absolute path shall be computed using the following expression: os.path.join(os.getcwd(),s_name_in_user_dir)
    #
    # @exception SavingSpreadSheetException if something has gone wrong while trying to write the spreadsheet into the aforementioned file

    def save_spreadsheet_to_file(self, s_name_in_user_dir):
        row_max_col = defaultdict(int)
        for coord in self.spreadsheet.cells:
            col_idx = Coordinate.column_to_number(coord.column_id)
            row_max_col[coord.row_id] = max(row_max_col[coord.row_id], col_idx + 1)

        try:
            file_path = os.path.join(os.getcwd(), s_name_in_user_dir)
            serialized = []

            for row in sorted(row_max_col):
                max_col = row_max_col[row]-1
                row_list = []
                # de 0..max_col-1
                for c in range(max_col):
                    letter = Coordinate.index_to_letter(c)
                    cell_coord = Coordinate(letter, row)
                    cell = self.spreadsheet.get_cell(cell_coord)

                    if cell is None:
                        row_list.append("")
                    else:
                        formula = cell.get_cell_formula()
                        if formula is not None:
                            row_list.append(formula)
                        else:
                            val = cell.get_cell_content()
                            row_list.append(str(val) if val is not None else "")
                serialized.append(row_list)
            SpreadsheetSave.save_to_s2v(serialized, file_path)
        except Exception as e:
            raise SavingSpreadsheetException(str(e))

    ##@brief Tries to load the spreadsheet from a file.
    #
    # @param s_name_in_user_dir  the local name of the file with respect to the folder where the invoking method is placed
    # (this is o because the markerrun shall look for files within the folder where testing classes are placed). The
    # absolute path shall be computed using the following expression: os.path.join(os.getcwd(),s_name_in_user_dir)
    #
    # @exception ReadingSpreadSheetException if something has gone wrong while trying to create spreadsheet and fill
    # it with the data present within the aforementioned file.

    def load_spreadsheet_from_file(self, s_name_in_user_dir):
        from utilities.SpreadsheetLoad import SpreadsheetLoad
        matrix = SpreadsheetLoad.read_file_as_matrix(s_name_in_user_dir)

        self.create_spreadsheet()

        # Rellenar contenidos usando self como controlador
        SpreadsheetLoad.load_spreadsheet(self, matrix)
        
        # badSpreadsheetLoad.load_spreadsheet(self, s_name_in_user_dir)