class PapiHubException(Exception):
    pass


class ParserException(PapiHubException):
    pass


class ParserFieldException(ParserException):
    def __init__(self, field_name: str, *args):
        super().__init__(*args)
        self.field_name = field_name
