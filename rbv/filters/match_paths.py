from ..file_utils import pattern_matches


def match_single_path(filepath, context):
    context.extend(pattern_matches(filepath))


def match_list_path(filepath_list, context):
    for fp in filepath_list:
        context.extend(pattern_matches(fp))


def match_file_paths(file_filepaths, context):
    with open(file_filepaths, "r") as ffile:
        filepaths = [line.rstrip("\n") for line in ffile]
    match_list_path(filepaths, context)
