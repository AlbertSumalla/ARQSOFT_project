# entities/errors/exceptions.py

# Base Exceptions
class SpreadsheetError(Exception):
    """Base error for the spreadsheet system."""
    pass

# ----------- FORMULAS ----------------

class FormulaSyntaxError(SpreadsheetError):
    """Syntax error while analyzing a formula."""
    pass

class TokenizationError(SpreadsheetError):
    """Error during the tokenization process."""
    pass

class PostfixGenerationError(SpreadsheetError):
    """Error while generating the postfix expression."""
    pass

class EvaluationError(SpreadsheetError):
    """General error during formula evaluation."""
    pass

class InvalidFunctionError(SpreadsheetError):
    """Unknown or unsupported function."""
    pass

class FunctionArgumentError(SpreadsheetError):
    """Invalid arguments provided to a function."""
    pass

# ----------- REFERENCES AND CELLS ----------------

class InvalidCellReferenceError(SpreadsheetError):
    """Reference to a non-existent or malformed cell."""
    pass

class DivisionByZeroError(SpreadsheetError):
    """Division by zero during formula evaluation."""
    pass

class CircularDependencyError(SpreadsheetError):
    """Circular dependency detected among cells."""
    pass

# ----------- FILES AND SERIALIZATION ----------------

class FileNotFoundError(SpreadsheetError):
    """The specified file could not be found."""
    pass

class PathError(SpreadsheetError):
    """Error saving the file to the specified path."""
    pass

class S2VFormatError(SpreadsheetError):
    """Invalid format encountered while parsing the S2V file."""
    pass

class SerializationError(SpreadsheetError):
    """Error while serializing spreadsheet content."""
    pass

# ----------- INITIALIZATION ----------------

class InvalidSizeError(SpreadsheetError):
    """Invalid size provided when initializing the spreadsheet."""
    pass

# ----------- MARKER ----------------

class BadCoordinateException(SpreadsheetError):
    """
    Raised when a cell reference is invalid or malformed.
    """
    pass

class ContentException(SpreadsheetError):
    """
    Raised when a formula or content string is syntactically or semantically incorrect.
    """
    pass

class CircularDependencyException(SpreadsheetError):
    """
    Raised when a formula introduces a circular dependency among cells.
    """
    pass

class NoNumberException(SpreadsheetError):
    """
    Raised when trying to get a numeric value from a non-numeric cell.
    """
    pass

class SavingSpreadSheetException(SpreadsheetError):
    """
    Raised when an error occurs saving the spreadsheet to a file.
    """
    pass

class ReadingSpreadSheetException(SpreadsheetError):
    """
    Raised when an error occurs loading the spreadsheet from a file.
    """
    pass

