from ..exceptions import IncorrectFileCount
from ..file_utils import filepath_exists


def count(n, context):
    """
    Action `count` checks that the context created by the filters
    respects the cardinality ``n``.

    Args:
        n(int): Requested number of files.
        context(list): the filtered context, e.g. all files to apply this rule to.

    Possible errors:
        single :class:`IncorrectFileCount`

    Example:

        * If the context matches the cardinality `n`, (e.g. 1 file for `n==1` or 7 `n=='+'`):
            `returns (True, [])`
        * If the context does not match the cardinality `n`, (e.g. 2 files for `n==1`):
            `returns (False, [IncorrectFileCount()])`

    Returns:
        tuple: (output boolean, error list)

    """

    existing_files = [filepath for filepath in context if filepath_exists(filepath)]
    if len(existing_files) != n:
        return False, [IncorrectFileCount(n, existing_files)]

    return True, []
