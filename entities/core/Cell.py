from ..core.Coordinate import Coordinate
from ..content.Content import Content

class Cell:
    def __init__(self, coordinate: Coordinate, content: Content):
        self.coordinate = coordinate
        self.content = content
        self.formula = None
        self.dependencies = set()

    def get_cell_content(self):
        return self.content.get_content() if self.content else None
    
    def get_cell_formula(self):
        return self.formula.evaluate()
        pass
    ##
    # @brief Stores the result of the formula in the cell.
    # @param cell: The target cell.
    # @param result The computed result to store.
    # @return None.
    def store_formula_and_result(cell, result):
        pass

