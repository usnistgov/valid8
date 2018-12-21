from rbv.filters.match_paths import (
    single_path,
    match_single_path,
    match_list_path,
    match_file_paths,
)
from rbv.context import Context

import os.path

# TODO make fixture that creates and destroys a fake file structure

simple_files = ["Makefile", "rbv", "test", "README.md"]
patterns = {"initpy": "test/*/__init__.py", "py": "**/*.py"}


def match_base_checks(result):
    assert result is not None
    assert type(result) is list
    for r in result:
        assert type(r) is Context


def test_single_match_paths():
    for f in simple_files:
        contexts = []
        match_single_path(filepath=f, contexts=contexts)
        match_base_checks(contexts)
        assert len(contexts) == 1, "This pattern must match a single file."
        assert os.path.basename(contexts[0].filepath) == f


def test_single_match_patterns():
    contexts = {k: [] for k in patterns.keys()}
    for k, v in contexts.items():
        match_single_path(filepath=patterns[k], contexts=v)

    for context in contexts.values():
        match_base_checks(context)
        assert len(context) > 1, "This pattern must match more than one file."

    for context in contexts["py"]:
        assert os.path.basename(context.filepath).endswith(".py")

    for context in contexts["initpy"]:
        assert os.path.basename(context.filepath) == "__init__.py"

    assert len(contexts["py"]) > len(contexts["initpy"])


def test_empty_match_pattern(tmpdir):
    match_str = str(tmpdir) + "/*"
    context = []
    match_single_path(filepath=match_str, contexts=context)
    match_base_checks(context)
    assert len(context) == 0, "This pattern must not match any files."


# def test_match_patterns_with_filepath():
#
#     single_match = match_paths(filepath=simple_files[0])
#     match_base_checks(single_match)
#     assert len(single_match) == 1, "This pattern must match a single file."
#     assert os.path.basename(single_match[0].filepath) == simple_files[0]
#
#     pattern_match = match_paths(filepath=patterns["py"])
#     match_base_checks(pattern_match)
#     for result in pattern_match:
#         assert os.path.basename(result.filepath).endswith(".py")


def test_match_patterns_with_list_filepaths():
    context = []
    match_list_path(filepath_list=simple_files, contexts=context)
    match_base_checks(context)
    assert len(context) == len(simple_files)
