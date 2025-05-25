from ..content.Content import Content

class NumericContent(Content):
    def __init__(self, number: float):
        self.number = number

    def get_content(self):
        return self.number

