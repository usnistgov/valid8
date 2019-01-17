from pathlib import Path

from ..exceptions import PatternNotFound
from ..file_utils import pattern_exists


# for every single context item
# 1) set certain variables, e.g. $DIRNAME
# 2) substitute those variables in match_pattern
# 3) check whether there is a file matching that pattern
#
def match(match_pattern, context):
    """"""
    outputs = list()
    errors = list()
    for filepath in context:
        s_ouptut, s_errors = single_match(match_pattern, filepath)
        outputs.append(s_ouptut)
        errors.extend(s_errors)

    # rv = (
    #     all([r[0] for r in result]),
    #     [error for errorlist in result[1] for error in errorlist],
    # )
    # print(type(rv), len(rv))
    # print(rv)
    # return (
    #     all([r[0] for r in result]),
    #     [error for errorlist in result[1] for error in errorlist],
    # )
    return all(outputs), errors


def single_match(match_pattern, context_filepath):
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
    context_path = Path(context_filepath)
    variables = {
        "DIR_NAME": context_path.parent.name,
        "DIR_PATH": context_path.parent,
        "FILENAME_NOEXT": context_path.stem,
        "FILENAME": context_path.name,
        "FILEPATH": context_path,
    }
    return variables
