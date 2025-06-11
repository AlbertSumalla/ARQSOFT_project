from .SpreadsheetController import *

class Coordinate:
    def __init__(self, column_id: str, row_id: int):
        self.column_id = column_id.upper()
        self.row_id = row_id

    def __str__(self):
        return f"{self.column_id}{self.row_id}"
    
    @staticmethod
    def index_to_letter(i: int) -> str:
        return chr(ord('A') + i - 1)