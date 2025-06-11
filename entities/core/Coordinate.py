from .SpreadsheetController import *

class Coordinate:
    def __init__(self, column_id: str, row_id: int):
        self.column_id = column_id
        self.row_id = row_id

    def __str__(self):
        return f"{self.column_id}{self.row_id}"
    
    @staticmethod
    def index_to_letter(i: int) -> str:
        return chr(ord('A') + i - 1)
    
    @classmethod
    def from_string(cls, s: str) -> "Coordinate":
        letter = ''.join(filter(str.isalpha, s)).upper()
        number = int(''.join(filter(str.isdigit, s)))
        col = ord(letter) - ord('A') + 1
        return cls(number, col)