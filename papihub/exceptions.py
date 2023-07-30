class PapiHubException(Exception):
    pass


class ParserException(PapiHubException):
    pass


class ParserFieldException(ParserException):
    def __init__(self, field_name: str, *args):
        super().__init__(*args)
        self.field_name = field_name


class ParserConfigErrorException(ParserException):
    filepath: str

    def __init__(self, filepath: str, *args):
        super().__init__(*args)
        self.filepath = filepath


class NotAuthenticatedException(PapiHubException):
    def __init__(self, site_id: str, site_name: str, *args):
        super().__init__(*args)
        self.site_id = site_id
        self.site_name = site_name
