import re

class Coordinate:
    def __init__(self, column_id: str, row_id: int):
        self.column_id = column_id.upper()
        self.row_id = row_id

    def __str__(self):
        return f"{self.column_id}{self.row_id}"

    @staticmethod
    def from_string(coord_str: str) -> 'Coordinate':
        match = re.match(r"([A-Z]+)(\d+)", coord_str.upper())
        if not match:
            raise ValueError(f"Invalid coordinate format: {coord_str}")
        return Coordinate(match[1], int(match[2]))
