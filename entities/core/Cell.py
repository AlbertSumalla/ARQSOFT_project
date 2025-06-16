from ..core.Coordinate import Coordinate
from ..content.Content import Content
from typing import List
class Cell:
    def __init__(self, coordinate: Coordinate, content: Content):
        self.coordinate = coordinate
        self.content = content if content is not None else None
        self.formula = None
        self.dependencies : List[Coordinate] = []

    def get_cell_content(self):
        return self.content
    
    def set_content(self, content: Content):
        self.content = content

    def set_cell_dependencies(self, dependencies: List[Coordinate]):
        self.dependencies = dependencies

    def get_cell_dependencies(self):
        return self.dependencies

    def get_cell_formula(self):
        return self.formula

    ##
    # @brief Stores the result of the formula in the cell.
    # @param cell: The target cell.
    # @param result The computed result to store.
    # @return None.
    def store_formula(cell, formula):
        cell.content = formula