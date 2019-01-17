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
        * {FILENAME}: the filename without the extension, e.g. `c.txt` for `a/b/c.txt`
        * {FILEPATH}: the file path, e.g. `a/b/c.txt` for `a/b/c.txt`

    Args:
        match_pattern (str): pattern to check for, for each context item
        context (list): the context (list of file paths) found by the filters

    Returns:
        tuple: (
            output (boolean),
            errors (list)
        )

    Possible errors:
        :class:PatternNotFound for each pattern not found
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
    Called by :func:`match`, has the same substitution variables
    Args:
        match_pattern: pattern to check for
        context_filepath: a single context item (i.e. filepath),
                          can contain substitution keys, see :func:`match`

    For the single context item:
    1) compute certain variables, e.g. {DIR_NAME}
    2) substitute those variables in match_pattern
    3) check whether there is a file matching that pattern

    Returns:
        tuple: (
            output (boolean),
            errors (list)
        )
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
