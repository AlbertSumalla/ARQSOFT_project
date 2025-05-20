from Content import Content

class NumericContent(Content):
    def __init__(self, number: float):
        self.number = number

    def evaluate(self):
        return self.number

