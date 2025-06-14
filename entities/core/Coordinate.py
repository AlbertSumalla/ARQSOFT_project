from .SpreadsheetController import *
import re
from typing import Match

class Coordinate:
    def __init__(self, column_id: str, row_id: int):
        self.column_id = column_id
        self.row_id = row_id


    def __eq__(self, other):
        return (
            isinstance(other, Coordinate)
            and self.column_id == other.column_id
            and self.row_id    == other.row_id
        )

    def __hash__(self):
        return hash((self.column_id, self.row_id))

    def __str__(self):
        return f"{self.column_id}{self.row_id}"

    @staticmethod
    def column_to_number(col: str) -> int:
        total = 0
        for char in col:
            total = total * 26 + (ord(char) - ord('A') + 1)
        return total
    
    @staticmethod
    def number_to_column(n: int) -> str:
        result = ""
        while n > 0:
            n, rem = divmod(n - 1, 26)
            result = chr(ord('A') + rem) + result
        return result

    @staticmethod
    def index_to_letter(i: int) -> str:
        return chr(ord('A') + i)
    
    @classmethod
    def from_string(cls, s: str) -> "Coordinate":
        m: Match | None = re.fullmatch(r"([A-Za-z]+)(\d+)", s.strip())
        if not m:
            raise ValueError(f"Formato de coordenada inválido: {s!r}")
        column_part, row_part = m.groups()
        return Coordinate(column_part.upper(), int(row_part))