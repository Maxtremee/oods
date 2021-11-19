class Filter:
    def __init__(self, attr: str, operator: str, value: any):
        self.attr: str = attr
        self.operator = operator
        self.value = value

class FilterBuilder:
    def __init__(self) -> None:
        self.argument = ''
        self.operator = 'eq'
        self.value = None

    def where(self, argument):
        self.argument = argument
        return self

    def eq(self, value):
        self.operator = 'eq'
        self.value = value
        return self

    def ne(self, value):
        self.operator = 'ne'
        self.value = value
        return self

    def lt(self, value):
        self.operator = 'lt'
        self.value = value
        return self

    def gt(self, value):
        self.operator = 'gt'
        self.value = value
        return self

    def le(self, value):
        self.operator = 'le'
        self.value = value
        return self

    def ge(self, value):
        self.operator = 'ge'
        self.value = value
        return self

    def build(self):
        return Filter(self.argument, self.operator, self.value)