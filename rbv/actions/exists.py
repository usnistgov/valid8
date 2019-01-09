import pathlib

from rbv.exceptions import NoSuchFile


class Output(dict):
    def __init__(self, output, exceptions=None):
        super().__init__()
        self.output = output
        self.exceptions = exceptions

    # init from iter of Results
    # append method (result+= result) using update


def exists(_boolean, context):
    result = list()

    def single_check(filepath):
        cpath = pathlib.Path(filepath)
        if cpath.exists():
            return Output(output=True, exceptions=[])
        return Output(output=False, exceptions=[NoSuchFile(target=filepath)])

    for filepath in context:
        result.append(single_check(filepath))

    # TODO need to review output type
    return (
        all([r.output for r in result]),
        [e for r in result for e in r.exceptions],
        [],
    )
