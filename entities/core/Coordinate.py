from ..core.SpreadsheetController import *
import re

class Coordinate:
    def __init__(self, column_id: str, row_id: int):
        self.column_id = column_id.upper()
        self.row_id = row_id

    def __str__(self):
        return f"{self.column_id}{self.row_id}"