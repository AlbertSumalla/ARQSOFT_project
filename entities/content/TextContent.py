from Content import Content

class TextContent(Content):
    def __init__(self, text: str):
        self.text = text

    def evaluate(self):
        return self.text

    def evaluate_as_number(self):
        if self.text.strip() == "":
            return 0
        try:
            return float(self.text)
        except ValueError:
            raise ValueError("Cannot convert text to number")
