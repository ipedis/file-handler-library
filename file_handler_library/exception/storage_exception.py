class InvalidStorageTypeException(Exception):
    def __init__(self, message: str | None = None):
        if message is None:
            message = 'Invalid storage type requested.'
        super().__init__(message)


class FileNotFoundException(Exception):
    def __init__(self, message: str | None = None):
        if message is None:
            message = 'Requested file not found.'
        super().__init__(message)


class NotADirectoryException(Exception):
    def __init__(self, message: str | None = None):
        if message is None:
            message = 'Given path is not a directory.'
        super().__init__(message)
