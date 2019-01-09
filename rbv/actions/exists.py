import pathlib

from rbv.exceptions import NoSuchFile


def exists(_boolean, context):
    result = list()

    def single_check(filepath):
        cpath = pathlib.Path(filepath)
        if cpath.exists():
            return {"output": True, "errors": []}
        return {"output": False, "errors": [NoSuchFile(target=filepath)]}

    for filepath in context:
        result.append(single_check(filepath))

    # TODO need to review output type
    return (
        all([r["output"] for r in result]),
        [e for r in result for e in r["errors"]],
    )
