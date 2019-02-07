import os.path

import pytest

from rbv.filters.match_paths import match_single_path, match_list_path
from ..lib import compare_main_with_expected_output, CURRENT_FILE_REL

arg_single = """
- rulename: checks_with_scripts
  filters:
    find: {}
  actions:
    exists: True
"""
arg_list = """
- rulename: checks_with_scripts
  filters:
    find:
      - {}
      - {}
  actions:
    exists: True
"""
arg_file = """
- rulename: checks_with_scripts
  filters:
    find:
      file: {}
  actions:
    exists: True
"""
file_contents = """
{}
{}
"""

data_ok = [arg_single.format(pattern) for pattern in [CURRENT_FILE_REL, "'*.py'"]]
data_fails = [arg_single.format(pattern) for pattern in ["a/b"]]

data_list_ok = [
    arg_list.format(pattern1, pattern2)
    for pattern1 in [CURRENT_FILE_REL]
    for pattern2 in [CURRENT_FILE_REL.parent]
]
data_list_fails = [arg_list.format("fake file", CURRENT_FILE_REL)]


@pytest.mark.parametrize("file_from_content", data_ok, indirect=["file_from_content"])
def test_find_ok(file_from_content, capsys):
    test_args = ["test", "validate", file_from_content.as_posix()]
    compare_main_with_expected_output(test_args, True, capsys)


@pytest.mark.parametrize(
    "file_from_content", data_fails, indirect=["file_from_content"]
)
def test_find_fails(file_from_content, capsys):
    test_args = ["test", "validate", file_from_content.as_posix()]
    compare_main_with_expected_output(test_args, False, capsys)


@pytest.mark.parametrize(
    "file_from_content", data_list_ok, indirect=["file_from_content"]
)
def test_find_list_ok(file_from_content, capsys):
    test_args = ["test", "validate", file_from_content.as_posix()]
    compare_main_with_expected_output(test_args, True, capsys)


@pytest.mark.parametrize(
    "file_from_content", data_list_fails, indirect=["file_from_content"]
)
def test_find_list_fails(file_from_content, capsys):
    test_args = ["test", "validate", file_from_content.as_posix()]
    compare_main_with_expected_output(test_args, False, capsys)


@pytest.mark.parametrize(
    "find_file_contents",
    [file_contents.format(CURRENT_FILE_REL, CURRENT_FILE_REL.parent)],
)
def test_find_file_ok(find_file_contents, make_file_from_contents, capsys):
    find_file = make_file_from_contents(find_file_contents)
    yml_config = make_file_from_contents(arg_file.format(find_file))
    test_args = ["test", "validate", yml_config.as_posix()]
    print(test_args)
    # assert 1 == 1
    compare_main_with_expected_output(test_args, True, capsys)


######################


simple_files = ["Makefile", "rbv", "tests", "README.md"]
patterns = {"initpy": "tests/*/__init__.py", "py": "**/*.py"}


def match_base_checks(result):
    assert result is not None
    assert type(result) is list
    for r in result:
        assert type(r) is str


def test_single_match_paths():
    for f in simple_files:
        context = []
        match_single_path(filepath=f, context=context)
        match_base_checks(context)
        assert len(context) == 1, "This pattern must match a single file."
        assert os.path.basename(context[0]) == f


def test_single_match_patterns():
    data = {k: [] for k in patterns}
    for k, v in data.items():
        match_single_path(filepath=patterns[k], context=v)

    for context in data.values():
        match_base_checks(context)
        assert len(context) > 1, "This pattern must match more than one file."

    for context in data["py"]:
        assert os.path.basename(context).endswith(".py")

    for context in data["initpy"]:
        assert os.path.basename(context) == "__init__.py"

    assert len(data["py"]) > len(data["initpy"])


def test_empty_match_pattern(tmpdir):
    match_str = str(tmpdir) + "/*"
    context = []
    match_single_path(filepath=match_str, context=context)
    match_base_checks(context)
    assert len(context) == 0, "This pattern must not match any files."


def test_match_patterns_with_list_filepaths():
    context = []
    match_list_path(filepath_list=simple_files, context=context)
    match_base_checks(context)
    assert len(context) == len(simple_files)
