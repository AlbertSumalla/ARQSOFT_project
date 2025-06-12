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

    def set_range(self,cell_range_list: list) -> None:
        self.range = cell_range_list