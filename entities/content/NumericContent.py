from entities.content.Content import Content

class NumericContent(Content):
    def __init__(self, number: float):
        self.number = number

    def get_content(self) -> float:
        return self.number

