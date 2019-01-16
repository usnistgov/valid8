from ..exceptions import IncorrectFileCount
from .exists import _file_exists


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
