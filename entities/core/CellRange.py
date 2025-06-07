from Coordinate import Coordinate

class CellRange:
    """
    Contiene un rango de celdas definido por coordenadas inicial y final.

    Atributos:
        start (Coordinate): coordenada de inicio del rango.
        end   (Coordinate): coordenada de fin del rango.
    """
    def __init__(self, start: Coordinate, end: Coordinate) -> None:
        self.start = start
        self.end = end

    def get_start(self) -> Coordinate:
        """Devuelve la coordenada de inicio del rango."""
        return self.start

    def set_start(self, start: Coordinate) -> None:
        """Establece la coordenada de inicio del rango."""
        self.start = start

    def get_end(self) -> Coordinate:
        """Devuelve la coordenada de fin del rango."""
        return self.end

    def set_end(self, end: Coordinate) -> None:
        """Establece la coordenada de fin del rango."""
        self.end = end