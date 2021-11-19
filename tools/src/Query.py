class Query:
    '''Query object containing appropriate querying function name and required arguments'''
    def __init__(self, function_name: str, arguments: dict):
        self.function_name = function_name
        self.arguments = arguments
