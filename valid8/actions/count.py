from ..exceptions import IncorrectFileCount, InsufficientFileCount, UnknownArgument
from ..file_utils import filepath_exists
import re

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
    exists_file_count = len(existing_files)

    count_plus_num_match = re.match("(\d+)\+",str(n))
    # Case 1: we have n="<n>+" where <n> is an integer
    if(count_plus_num_match is not None):
        min_n = count_plus_num_match.group(1)
        if(exists_file_count >= min_n):
            return True, [],
        else:
            return False, [InsufficientFileCount(min_n, existing_files)]
    # Case 2: n is an integer parseable with int(), if here not at Case 1
    try:
        int_n = int(n)
        if exists_file_count != int_n:
            return False, [IncorrectFileCount(int_n, existing_files)]
        return True, []
    # Case 3: improperly formatted arugment
    except ValueError as e:
        err_message = "count() expects and integer or an integer followed by a plus, such as '11' or `3+`. " + \
                  "count() received argument " + n
        raise UnknownArgument(err_message, "action", "count")



