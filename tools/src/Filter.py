class Filter:
    '''Contains data for filtering'''
    def __init__(self, attr: str, operator: str, value: any):
        self.attr: str = attr
        self.operator = operator
        self.value = value

class FilterBuilder:
    '''Builder class for complex filtering queries'''
    def __init__(self) -> None:
        self.argument = ''
        self.operator = 'eq'
        self.value = None

    def where(self, argument):
        '''Accepts attribute name'''
        self.argument = argument
        return self

    def eq(self, value):
        '''Accepts value to which attribute should be equal to'''
        self.operator = 'eq'
        self.value = value
        return self

    def ne(self, value):
        '''Accepts value to which attribute should be not equal to'''
        self.operator = 'ne'
        self.value = value
        return self

    def lt(self, value):
        '''Accepts value to which attribute should be less than'''
        self.operator = 'lt'
        self.value = value
        return self

    def gt(self, value):
        '''Accepts value to which attribute should be greater than'''
        self.operator = 'gt'
        self.value = value
        return self

    def le(self, value):
        '''Accepts value to which attribute should less or equal to'''
        self.operator = 'le'
        self.value = value
        return self

    def ge(self, value):
        '''Accepts value to which attribute should be greater or equal to'''
        self.operator = 'ge'
        self.value = value
        return self

    def build(self):
        '''Returns Filter object'''
        return Filter(self.argument, self.operator, self.value)