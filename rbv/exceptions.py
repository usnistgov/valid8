class BaseValidationError(Exception):
    def __init__(self, message, *args):
        self.message = message
        super().__init__(message, *args)

    def __str__(self):
        return self.message


class NoSuchFile(BaseValidationError):
    def __init__(self, filepath):
        self.target = filepath
        self.message = f"'{filepath}' was not found."
        super().__init__(self.message)


class IncorrectFileCount(BaseValidationError):
    def __init__(self, requested_count, files_found):
        self.requested_count = requested_count
        self.files_found = files_found
        self.message = f"{len(files_found)} files found, {requested_count} requested."
        super().__init__(self.message)


class UnknownRule(BaseValidationError):
    """"""

    def __init__(self, rule):
        self.rule = rule
        self.message = f"'{rule}' was not recognized."
        super().__init__(self.message)


class PatternNotFound(BaseValidationError):
    def __init__(self, pattern, before_subs=None):
        self.target = pattern
        self.message = f"Pattern '{pattern}' not found."
        self.before_subs = before_subs
        super().__init__(self.message, self.before_subs)


# TODO could dataclasses be useful here?
