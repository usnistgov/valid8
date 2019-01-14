import pathlib

from ..exceptions import NoSuchFile, IncorrectFileCount


def _file_exists(filepath):
    """
    Checks for file existence. Works for any file type, including directories.
    Uses pathlib library.

    Args:
        filepath(str): File path to ttest for existence

    Returns: (bool) whether the file exists

    """
    cpath = pathlib.Path(filepath)
    return cpath.exists()


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
        if _file_exists(filepath):
            return {"output": True, "errors": []}
        return {"output": False, "errors": [NoSuchFile(target=filepath)]}

    for filepath in context:
        result.append(single_check(filepath))

    return (
        all([r["output"] for r in result]),
        [e for r in result for e in r["errors"]],
    )


def count(n, context):
    """
    Action `count`

    Args:
        n(int): Exact requested number of files.
        context(list):

    Returns: tuple
            (True, []) if exactly `n` existing files from context were found
            (False, error_list) if not.

    Possible errors: single IncorrectFileCount
    """

    existing_files = [filepath for filepath in context if _file_exists(filepath)]
    if len(existing_files) != n:
        return False, [IncorrectFileCount(n, existing_files)]

    return True, []
