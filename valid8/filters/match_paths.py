# Contents subject to LICENSE.txt at project root

from ..exceptions import UnknownArgument
from ..file_utils import pattern_matches


def find(args, context, **kwargs):
    if len(args) > 0 and len(kwargs) == 0:

        if isinstance(args, str):
            match_single_path(args, context)

        else:
            match_list_path(args, context)

    elif len(kwargs) > 0:
        file_filepaths = kwargs["file"]
        match_file_paths(file_filepaths, context)

    else:
        raise UnknownArgument(
            message="Arguments to find must be str, list or dict.",
            rule_type="filter",
            rule_name="find",
        )


def match_single_path(filepath, context):
    context.extend(pattern_matches(filepath))


def match_list_path(filepath_list, context):
    for fp in filepath_list:
        context.extend(pattern_matches(fp))


def match_file_paths(file_filepaths, context):
    with open(file_filepaths, "r") as ffile:
        filepaths = [line.rstrip("\n") for line in ffile]
    match_list_path(filepaths, context)
