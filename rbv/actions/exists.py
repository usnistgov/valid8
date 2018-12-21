from collections import deque
import pathlib


def RuleOutput(dict):
    def __init__(self):
        super().__init__()

    # key: rule name
    #

class Output(dict):

    def __init__(self, output, exceptions=None):
        super().__init__()
        self.output = output
        self.exceptions = exceptions
    # init from iter of Results
    # append method (result+= result) using update



class BaseValidationError(Exception):

    pass


class NoSuchFile(BaseValidationError):
    def __init__(self, target):
        self.target = target
        self.message = f"{target} was not found."


def exists(_boolean, contexts, type=None):
    """
    Checks that all contexts exits, and their type if specified
    :param contexts: list of contexts (e.g. matches files) to check for existence
    :type contexts: iterable<Context>
    :param type: (optional) type to check
    :type type: str
    :return:
    :rtype: bool
    """

    result = list()

    def single_check(context, type=None):
        cpath = pathlib.Path(context.filepath)
        if cpath.exists():
            return Output(output=True, exceptions=[])
        return Output(output=False, exceptions=[NoSuchFile(target=context.filepath)])

    for context in contexts:
        result.append(single_check(context))

    return all([r.output for r in result]), [e for r in result for e in r.exceptions], []
