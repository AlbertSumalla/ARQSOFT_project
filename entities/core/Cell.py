from ..core.Coordinate import Coordinate
from ..content.Content import Content

class Cell:
    def __init__(self, coordinate: Coordinate, content: Content):
        self.coordinate = coordinate
        self.content = content
        self.formula = None
        self.dependencies = set()

    def get_cell_content(self):
        return self.content
    
    def set_cell_content(self, content: Content):
        self.content = content
        
    def get_cell_formula(self):
        return self.formula

    ##
    # @brief Stores the result of the formula in the cell.
    # @param cell: The target cell.
    # @param result The computed result to store.
    # @return None.
    def store_formula(cell, formula):
        cell.content = formula