# entities/errors/exceptions.py

# Excepciones base
class SpreadsheetError(Exception):
    """Error base del sistema de hoja de cálculo."""
    pass

# ----------- FÓRMULAS ----------------

class FormulaSyntaxError(SpreadsheetError):
    """Error de sintaxis al analizar una fórmula."""
    pass

class TokenizationError(SpreadsheetError):
    """Error durante el proceso de tokenización."""
    pass

class PostfixGenerationError(SpreadsheetError):
    """Error al generar la expresión en notación postfija."""
    pass

class EvaluationError(SpreadsheetError):
    """Error general durante la evaluación de una fórmula."""
    pass

class InvalidFunctionError(SpreadsheetError):
    """Función desconocida o no soportada."""
    pass

class FunctionArgumentError(SpreadsheetError):
    """Error en los argumentos de una función."""
    pass


# ----------- REFERENCIAS Y CELDAS ----------------

class InvalidCellReferenceError(SpreadsheetError):
    """Referencia a una celda inexistente o mal formada."""
    pass

class DivisionByZeroError(SpreadsheetError):
    """División por cero durante la evaluación de una fórmula."""
    pass

class CircularDependencyError(SpreadsheetError):
    """Dependencia circular detectada entre celdas."""
    pass


# ----------- ARCHIVOS Y SERIALIZACIÓN ----------------

class FileNotFoundError(SpreadsheetError):
    """El archivo especificado no se encuentra."""
    pass

class PathError(SpreadsheetError):
    """Error al guardar el archivo en la ruta especificada."""
    pass

class S2VFormatError(SpreadsheetError):
    """Error de formato al parsear un archivo S2V."""
    pass

class SerializationError(SpreadsheetError):
    """Error al serializar el contenido del spreadsheet."""
    pass



class InvalidSizeError(SpreadsheetError):
    """Tamaño inválido al inicializar un spreadsheet."""
    pass
