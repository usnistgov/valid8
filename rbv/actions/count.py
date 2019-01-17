from ..exceptions import IncorrectFileCount
from ..file_utils import filepath_exists


def count(n, context):
    """
    Action `count`

    Args:
        n(int): Exact requested number of files.
        context(list): the filtered context, e.g. all files to apply this rule to.

    Returns: tuple
            (True, []) if exactly `n` existing files from context were found
            (False, error_list) if not.

    Possible errors: single IncorrectFileCount
    """

    existing_files = [filepath for filepath in context if filepath_exists(filepath)]
    if len(existing_files) != n:
        return False, [IncorrectFileCount(n, existing_files)]

    return True, []
