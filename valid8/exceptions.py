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


class InsufficientFileCount(BaseValidationError):
    def __init__(self, requested_count, files_found):
        self.requested_count = requested_count
        self.files_found = files_found
        self.message = (
            f"{len(files_found)} files found, at least {requested_count} requested."
        )
        super().__init__(self.message)


class IncorrectFileCount(BaseValidationError):
    def __init__(self, requested_count, files_found):
        self.requested_count = requested_count
        self.files_found = files_found
        self.message = f"{len(files_found)} files found, {requested_count} requested."
        super().__init__(self.message)


class UnknownRule(BaseValidationError):
    def __init__(self, type, name):
        self.type = type
        self.name = name
        self.message = f"{type}-{name} was not recognized."
        super().__init__(self.message)


class UnknownArgument(BaseValidationError):
    def __init__(self, message, rule_type, rule_name):
        self.rule_type = rule_type
        self.rule_name = rule_name
        super().__init__(message)


class PatternNotFound(BaseValidationError):
    def __init__(self, pattern, before_subs=None):
        self.target = pattern
        self.message = f"Pattern '{pattern}' not found."
        self.before_subs = before_subs
        super().__init__(self.message, self.before_subs)


class ValidationSyntaxError(BaseValidationError):
    def __init__(self, exception):
        self.exception = exception
        self.message = f"Found incorrect syntax. Exception raised {exception}"
        super().__init__(self.message, self.exception)
