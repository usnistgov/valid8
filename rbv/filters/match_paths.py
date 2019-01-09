from glob import glob


def single_path(filepath):
    # if is exact path, e.g. no *, also add Path(filepath)
    # replace this when '*' is not the only regex char and when escaping is introduced.
    def is_exact_path(filepath):
        return "*" not in filepath

    if is_exact_path(filepath):
        return [filepath]

    glob_matches = glob(filepath, recursive=True)
    return [match for match in glob_matches]


def match_single_path(filepath, context):
    context.extend(single_path(filepath))


def match_list_path(filepath_list, context):
    for fp in filepath_list:
        context.extend(single_path(fp))


def match_file_paths(file_filepaths, context):
    with open(file_filepaths, "r") as ffile:
        filepaths = [line.rstrip("\n") for line in ffile]
    match_list_path(filepaths, context)
