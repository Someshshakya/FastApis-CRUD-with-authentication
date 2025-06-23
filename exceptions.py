class NotFoundException(Exception):
    def __init__(self, detail: str):
        self.detail = detail

class BadRequestException(Exception):
    def __init__(self, detail: str):
        self.detail = detail

class DatabaseException(Exception):
    def __init__(self, detail: str = "Internal Server Error"):
        self.detail = detail
