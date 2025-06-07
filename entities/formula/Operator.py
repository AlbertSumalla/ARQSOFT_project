class Operator:

    def __init__(self, operator: str) -> None:
        self.operator: str = operator

    def get_operator(self) -> str:
        return self.operator

    def set_operator(self, operator: str) -> None:
        self.operator = operator