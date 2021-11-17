class Filter:
    def __init__(self, attr: str, operator: str, value: any):
        self.attr: str = attr
        self.operator = operator
        self.value = value