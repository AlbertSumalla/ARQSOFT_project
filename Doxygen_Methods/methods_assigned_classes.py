class Spreadsheet:

    ##
    # @brief Resolves the value of a referenced cells.
    # @param Spreadsheet: The spreadsheet object containing cells.
    # @param coordinate: The cell reference that has changed
    # @return None
    def resolve_cell_references(spreadsheet,coordinate):
        pass

    ##
    # @brief Updates all cells that depend on a modified cell.
    # @param cell: The cell whose value was updated.
    # @exception CircularDependencyError Raised if a circular dependency is found.
    # @exception InvalidCellReferenceError Raised if a dependency is invalid.
    # @return None.
    def update_dependent_cells(cell):
        pass

    ##
    # @brief Updates all cells and dependencies after importing a file.
    # @param Spreadsheet: The spreadsheet instance to which cells have to be updated.
    # @return None.
    def update_cell_values(spreadsheet):
        pass

    ##
    # @brief Scans the spreadsheet to detect any circular dependencies among cells.
    # @param Spreadsheet: The spreadsheet instance.
    # @exception CircularDependencyError Raised if circular dependencies are found.
    # @return None
    def identify_circular_dependencies(spreadsheet):
        pass

class SpreadsheetFactory:
    
    ##
    # @brief Creates a 2D matrix of empty cells for the spreadsheet with specific size.
    # @param rows Number of rows.
    # @param columns Number of columns.
    # @exception InvalidSizeError Raised if rows or columns are negative or zero.
    # @return Spreadsheet: Returns the spreadsheet instance. 
    def initialize_spreadsheet(rows, columns):
        pass

class ShuntingYard:

    ##
    # @brief System generates a postfix expression using Shunting-Yard.
    # @param tokens_list: List of tokens, Token[] array 
    # @exception PostfixError Raised if postfix generation fails.
    # @return postfix_exp: Expression with a combination of operands and opeators.
    def generate_postfix_expression(tokens_list):
        pass

class Cell:

    ##
    # @brief Stores the result of the formula in the cell.
    # @param cell: The target cell.
    # @param result The computed result to store.
    # @return None.
    def store_formula_and_result(cell, result):
        pass

class Function:

    ##
    # @brief Evaluates a Function object
    # @param function: A string of the function to be evaluated.
    # @return A numeric result of the function.
    def compute_function(function):
        pass


class SpreadsheetController:

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


class UserInterface:

    ##
    # @brief Terminates the application, releasing all resources.
    # @return None.
    def exit_program():
        pass

    ##
    # @brief Displays the formula defined in a specific cell.
    # @param Cell: cell The coordinates or identifier of the cell.
    # @return None
    def display_cell_formula(cell):
        pass

    ##
    # @brief Displays a menu of available options in the console.
    # @return None
    def display_menu():
        pass


class SpreadsheetShow:
    ##
    # @brief Displays the empty spreadsheet in the console.
    # @param spreadsheet The spreadsheet instance.
    # @return None.
    def display_spreadsheet(spreadsheet):
        pass

class ContentFactory:

    ##
    # @brief Converts the user input into a Content object.
    # @param input_string: The raw content from user.
    # @param content_type: Result from identify_input_type()
    # @return Content_object: object (TextContent, NumericContent, or FormulaContent).
    def create_content_object(input_string, content_type):
        pass


class Tokenizer:

    ##
    # @brief Tokenizes the formula that is on a selected cell.
    # @param formula_str: The formula string from the cell.
    # @return tokens_list: string list.
    def tokenize_formula(formula_str):
        pass


class SpreadsheetLoad:

    ##
    # @brief Loads and parses a spreadsheet from an S2V file.
    # @param file_path Path to the S2V file.
    # @exception FileNotFoundError Raised if file does not exist.
    # @exception S2VFormatError Raised if the file format is incorrect.
    # @return Spreadsheet: The instance of the spreadsheet.
    def load_spreadsheet(file_path):
        pass

    ##
    # @brief Parses one line and updates the corresponding row of the spreadsheet
    # @param file_line: A line that has to be parsed.
    # @return None.
    def parse_s2v_line(file_line):
        pass


class FormulaParser:

    ##
    # @brief Parses and checks the syntax of the formula string.
    # @param tokens_list: List of tokens, Token[] array 
    # @exception SyntaxError Raised if the syntax is invalid.
    # @return None
    def parse_formula(tokens_list):
        pass


class FormulaProcess:

    ##
    # @brief Evaluates a postfix expression to extract its result.
    # @param postfix_exp: Postfix expression that has to be resolved.
    # @param spreadsheet: The Spreadsheet object containing the referenced cells.
    # @exception InvalidCellReference Raised for non-existent cells or invalid value.
    # @exception DivisionByZeroError Raised on division by zero.
    # @return Result: Int/Real value after computing the evaluation.
    def evaluate_postfix_expression(postfix_exp, spreadsheet):
        pass


class SpreadsheetSave:

    ##
    # @brief Saves the spreadsheet to a file in S2V format.
    # @param serial_rows: The Spreadsheet serialized in rows.
    # @param file_path Path where the S2V file will be saved.
    # @exception PathError Raised if the file cannot be saved correctly.
    # @return None.
    def save_to_s2v(serial_rows, file_path):
        pass
