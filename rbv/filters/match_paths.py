from glob import glob
from pathlib import Path

from ..context import Context


def single_path(filepath):
    # if is exact path, e.g. no *, also add Path(filepath)
    # replace this when '*' is not the only regex char and when escaping is introduced.
    def is_exact_path(filepath):
        return '*' not in filepath

    if is_exact_path(filepath):
        return [Context(filepath=filepath)]

    glob_matches = glob(filepath, recursive=True)
    return [Context(filepath=match) for match in glob_matches]


def match_single_path(filepath, contexts):
    contexts.extend(single_path(filepath))


def match_list_path(filepath_list, contexts):
    for fp in filepath_list:
        contexts.extend(single_path(fp))


def match_file_paths(file_filepaths, contexts):
    with open(file_filepaths, "r") as ffile:
        filepaths = [line.rstrip("\n") for line in ffile]
    match_list_path(filepaths, contexts)
