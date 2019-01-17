from ..exceptions import NoSuchFile
from ..file_utils import filepath_exists


def exists(_boolean, context):
    """ Action `exists` will check that every item in the context does exist.

    Args:
        _boolean: Placeholder for now. Holds the `True` value from the `exists: True` statement
        context: The dict holding the filtered context, e.g. all files to apply this rule to.

    Returns: tuple
            (True, []) if all files were found.
            (False, error_list) if not.

    Possible errors: NoSuchFile for each item in context not found.
    """
    result = list()

    def single_check(filepath):
        if filepath_exists(filepath):
            return {"output": True, "errors": []}
        return {"output": False, "errors": [NoSuchFile(filepath=filepath)]}

    for filepath in context:
        result.append(single_check(filepath))

    return (
        all([r["output"] for r in result]),
        [e for r in result for e in r["errors"]],
    )
