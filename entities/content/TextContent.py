from ..content.Content import Content

class TextContent(Content):
    def __init__(self, text: str):
        self.text = text

    def evaluate(self):
        return self.text
