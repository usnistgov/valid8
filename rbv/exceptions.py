class BaseValidationError(Exception):
    pass


class NoSuchFile(BaseValidationError):
    def __init__(self, target):
        self.target = target
        self.message = f"{target} was not found."


class IncorrectFileCount(BaseValidationError):
    def __init__(self, requested_count, files_found):
        self.requested_count = requested_count
        self.files_found = files_found
        self.message = f"{len(files_found)} files found, {requested_count} requested."
