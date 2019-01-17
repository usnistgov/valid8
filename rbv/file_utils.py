import pathlib
from glob import glob


def pattern_matches(pattern):
    """
    Uses glob to find all the file paths that `pattern` may match.
    DOES NOT garantee file existence.

    Args:
        pattern (str or Path-like): file path, can include wildcards

    Returns:
        list: of pattern matches.
        If not using regex/wildcards, will return [pattern], whether or not `pattern` exists.
    """
    # if is exact path, e.g. no *, also add Path(filepath)
    # replace this when '*' is not the only regex char and when escaping is introduced.
    def is_exact_path():
        return "*" not in pattern

    if is_exact_path():
        return [pattern]

    glob_matches = glob(pattern, recursive=True)
    return [match for match in glob_matches]


def filepath_exists(filepath):
    """
    Checks for file existence. Works for any file type, including directories.
    Uses pathlib library.

    Args:
        filepath(str): File path to test for existence

    Returns: (bool) whether the file exists

    """
    cpath = pathlib.Path(filepath)
    return cpath.exists()


def pattern_exists(pattern):
    """
    Uses glob to find all EXISTING files that match `pattern`.

    Args:
        pattern (str or Path-like): file path, can include wildcards

    Returns:
        list: of existing pattern matches.
    """
    matches = pattern_matches(pattern)
    return [f for f in matches if filepath_exists(f)]
