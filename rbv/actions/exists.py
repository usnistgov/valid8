import pathlib

from ..exceptions import BaseValidationError


class Output(dict):
    def __init__(self, output, exceptions=None):
        super().__init__()
        self.output = output
        self.exceptions = exceptions

    # init from iter of Results
    # append method (result+= result) using update


class NoSuchFile(BaseValidationError):
    def __init__(self, target):
        self.target = target
        self.message = f"{target} was not found."


def exists(_boolean, contexts):
    """

    Args:
        _boolean ():
        contexts ():

    Returns:

    """
    result = list()

    def single_check(context):
        cpath = pathlib.Path(context.filepath)
        if cpath.exists():
            return Output(output=True, exceptions=[])
        return Output(output=False, exceptions=[NoSuchFile(target=context.filepath)])

    for context in contexts:
        result.append(single_check(context))

    # need to review output type
    return (
        all([r.output for r in result]),
        [e for r in result for e in r.exceptions],
        [],
    )
