class BaseValidationError(Exception):
    pass


class NoSuchFile(BaseValidationError):
    def __init__(self, target):
        self.target = target
        self.message = f"{target} was not found."
