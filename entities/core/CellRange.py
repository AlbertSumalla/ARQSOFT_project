from Coordinate import Coordinate

class CellRange:
    def __init__(self, start: Coordinate, end: Coordinate) -> None:
        self.start = start
        self.end = end
        self.range = list()

    def get_start(self) -> Coordinate:
        return self.start

    def set_start(self, start: Coordinate) -> None:
        self.start = start

    def get_end(self) -> Coordinate:
        return self.end

    def set_end(self, end: Coordinate) -> None:
        self.end = end

    def get_range(self) -> list:
        '''recorrer la spreadsheet y obtener la lista de coordenadas, se tiene que hacer un bucle'''