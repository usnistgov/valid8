from pathlib import Path

from ..exceptions import PatternNotFound
from ..file_utils import pattern_exists


def match(match_pattern, context):
    """
    Action `match` checks that files represented by a pattern are
    present for every context item.

    In addition to syntax recognized by glob, the following variables are
    recognized in the pattern for each context item:

        * {DIR_NAME}: the directory name, e.g. `b` for `a/b/c.txt`
        * {DIR_PATH}: the directory path for a context path, e.g. `a/b` for `a/b/c.txt`
        * {FILENAME_NOEXT}: the filename without the extension, e.g. `c` for `a/b/c.txt`
        * {FILENAME}: the filename with the extension, e.g. `c.txt` for `a/b/c.txt`
        * {FILEPATH}: the file path, e.g. `a/b/c.txt` for `a/b/c.txt`

    Possible errors:
        :class:PatternNotFound for each pattern not found

    Example:

        * If a match is found for every context item:
            ``returns (True, [])``
        * If a match is found for all but one context item:
            ``returns (False, [PatternNotFound()])``

    Args:
        match_pattern (str): pattern to check for, for each context item
        context (list): the context (list of file paths) found by the filters

    Returns:
        tuple: (output boolean, error list)

    """
    outputs = list()
    errors = list()
    for filepath in context:
        s_ouptut, s_errors = single_match(match_pattern, filepath)
        outputs.append(s_ouptut)
        errors.extend(s_errors)

    return all(outputs), errors


def single_match(match_pattern, context_filepath):
    """
    Checks that files matched by a single pattern are present.
    Called by :func:`match`, supports the same substitution variables
    in ``context_filepath``.

    For the single context item:

    #. compute certain variables, e.g. {DIR_NAME}
    #. substitute those variables in match_pattern
    #. check whether there is a file matching that pattern

    Args:
        match_pattern (str): pattern to check for
        context_filepath (str): a single context item (i.e. filepath)

    Returns:
        tuple: (output boolean, error list)

    """
    variables = context_variables(context_filepath)
    interpreted_pattern = match_pattern.format(**variables)
    matches = pattern_exists(interpreted_pattern)

    if len(matches) > 0:
        return True, []

    return (
        False,
        [PatternNotFound(pattern=interpreted_pattern, before_subs=match_pattern)],
    )


def context_variables(context_filepath):
    """
    Context file path subsitutions for :func:`match`

    Args:
        context_filepath: the file path that may contain substition keys

    Returns:
        dict: of all the substitution keys and their values
    """
    context_path = Path(context_filepath)
    variables = {
        "DIR_NAME": context_path.parent.name,
        "DIR_PATH": context_path.parent,
        "FILENAME_NOEXT": context_path.stem,
        "FILENAME": context_path.name,
        "FILEPATH": context_path,
    }
    return variables
