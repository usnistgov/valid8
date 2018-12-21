from rbv.filters.match_paths import match_paths, single_match_paths
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
        result = single_match_paths(filepath=f)
        match_base_checks(result)
        assert len(result) == 1, "This pattern must match a single file."
        assert os.path.basename(result[0].filepath) == f


def test_single_match_patterns():
    results = {k: single_match_paths(filepath=v) for k, v in patterns.items()}
    for result in results.values():
        match_base_checks(result)
        assert len(result) > 1, "This pattern must match more than one file."

    for result in results["py"]:
        assert os.path.basename(result.filepath).endswith(".py")

    for result in results["initpy"]:
        assert os.path.basename(result.filepath) == "__init__.py"

    assert len(results["py"]) > len(results["initpy"])


def test_empty_match_pattern(tmpdir):
    match_str = str(tmpdir) + "/*"
    empty_matches = single_match_paths(filepath=match_str)
    match_base_checks(empty_matches)
    assert len(empty_matches) == 0, "This pattern must not match any files."


def test_match_patterns_with_filepath():

    single_match = match_paths(filepath=simple_files[0])
    match_base_checks(single_match)
    assert len(single_match) == 1, "This pattern must match a single file."
    assert os.path.basename(single_match[0].filepath) == simple_files[0]

    pattern_match = match_paths(filepath=patterns["py"])
    match_base_checks(pattern_match)
    for result in pattern_match:
        assert os.path.basename(result.filepath).endswith(".py")


def test_match_patterns_with_list_filepaths():
    multi_match = match_paths(list_filepaths=simple_files)
    match_base_checks(multi_match)
    assert len(multi_match) == len(simple_files)
