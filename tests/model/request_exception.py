class RequestException(Exception):
    def __init__(self, code, message):
        self.code = code
        self.message = message

    def __str__(self) -> str:
        return f'{self.code}, {self.message}'

