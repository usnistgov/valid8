from collections import namedtuple

import pytest

from valid8.actions.match import context_variables, single_match, match


@pytest.mark.parametrize(
    "filepath, e_dirname, e_filename, e_filenamenoext",
    [
        ("hello/", "", "hello", "hello"),
        ("hello/world/", "hello", "world", "world"),
        ("hello/world", "hello", "world", "world"),
        ("hello/world/file.txt", "world", "file.txt", "file"),
    ],
)
def test_variables(filepath, e_dirname, e_filename, e_filenamenoext):
    variables = context_variables(filepath)
    assert variables["DIR_NAME"] == e_dirname
    assert variables["FILENAME"] == e_filename
    assert variables["FILENAME_NOEXT"] == e_filenamenoext


FilepathScenario = namedtuple(
    "FilepathScenario", "dirstructure, filepath, pattern, expected"
)
ContextScenario = namedtuple(
    "ContextScenario", "dirstructure, context, pattern, expected"
)
ds_data = {
    "empty": [],
    "simple": ["hello.txt"],
    "subdir": ["a/hello.txt"],
    "multi": ["a/hello.txt", "a/b/hello.txt", "a/b/world.txt", "b/hello.txt"],
}
scenarios_for_single_match = [
    # DIR_NAME
    FilepathScenario(
        ds_data["simple"], "a/somefile.txt", "{DIR_NAME}/hello.txt", False
    ),
    FilepathScenario(ds_data["subdir"], "a/somefile.txt", "{DIR_NAME}/hello.txt", True),
    FilepathScenario(ds_data["empty"], "a/somefile.txt", "{DIR_NAME}/hello.txt", False),
    FilepathScenario(
        ds_data["subdir"], "a/somefile.txt", "{DIR_NAME}/otherfile.txt", False
    ),
    FilepathScenario(
        ds_data["multi"], "a/somefile.txt", "{DIR_NAME}/otherfile.txt", False
    ),
    FilepathScenario(
        ds_data["multi"], "a/somefile.txt", "{DIR_NAME}/b/hello.txt", True
    ),
    FilepathScenario(
        ds_data["multi"] + ["a/somefile.txt"],
        "a/somefile.txt",
        "{DIR_NAME}/somefile.txt",
        True,
    ),
    FilepathScenario(
        ds_data["multi"], "a/somefile.txt", "{DIR_NAME}/somefile.txt", False
    ),
    # DIR_PATH
    FilepathScenario(
        ds_data["multi"], "a/b/somefile.txt", "{DIR_PATH}/world.txt", True
    ),
    FilepathScenario(ds_data["multi"], "a/world.txt", "a/{DIR_PATH}/hello.txt", False),
    # FILENAME_NOEXT
    FilepathScenario(ds_data["multi"], "a/b/world.txt", "a/b/{FILENAME_NOEXT}*", True),
    FilepathScenario(ds_data["multi"], "a/world.txt", "{FILENAME_NOEXT}", False),
    # FILENAME
    FilepathScenario(ds_data["multi"], "a/b/world.txt", "a/b/{FILENAME}*", True),
    FilepathScenario(ds_data["multi"], "a/b/world.txt", "a/b/{FILENAME}", True),
    FilepathScenario(ds_data["multi"], "a/world.txt", "{FILENAME}*", False),
    FilepathScenario(ds_data["multi"], "a/world.txt", "*/*/{FILENAME}*", True),
    # FILEPATH
    FilepathScenario(ds_data["multi"], "a/hello.txt", "{FILEPATH}", True),
    FilepathScenario(ds_data["multi"], "a/hello.txt", "*{FILEPATH}*", True),
    FilepathScenario(ds_data["multi"], "a/does.not.exist", "*{FILEPATH}*", False),
    # COMBINED
    FilepathScenario(
        ds_data["multi"], "a/b/hello.txt", "{DIR_NAME}/{FILENAME_NOEXT}*", True
    ),
    FilepathScenario(
        ds_data["multi"], "a/b/hello.txt", "{DIR_NAME}/*/{FILENAME_NOEXT}*", False
    ),
]
converted_scenarios_for_match = [
    ContextScenario(s.dirstructure, [s.filepath], *s[2:])
    for s in scenarios_for_single_match
]
scenarios_for_match = converted_scenarios_for_match + [
    ContextScenario(
        ds_data["multi"], ["a/world.txt", "a/b/world.csv"], "{DIR_NAME}/hello.txt", True
    ),
    ContextScenario(
        ds_data["multi"], ["a/world.txt", "a/b/world.csv"], "{DIR_PATH}/hello.txt", True
    ),
    ContextScenario(
        ds_data["multi"], ["a/world.txt", "a/b/world.csv"], "{DIR_PATH}/hello.txt", True
    ),
    ContextScenario(
        ds_data["multi"],
        ["a/world.txt", "a/b/world.txt", "c/world.txt"],
        "{DIR_NAME}/hello.txt",
        False,
    ),
]


@pytest.mark.parametrize(
    "dirstructure, filepath, pattern, expected",
    scenarios_for_single_match,
    indirect=["dirstructure"],
)
def test_single_match(dirstructure, filepath, pattern, expected):
    output, errors = single_match(pattern, filepath)
    if expected is True:
        assert output is True
        assert len(errors) == 0
    else:
        assert output is False
        assert len(errors) == 1
        assert errors[0].before_subs == pattern


@pytest.mark.parametrize(
    "dirstructure, context, pattern, expected",
    scenarios_for_match,
    indirect=["dirstructure"],
)
def test_match(dirstructure, context, pattern, expected):

    output, errors = match(pattern, context)
    if expected is True:
        assert output is True
        assert len(errors) == 0
    else:
        assert output is False
        assert len(errors) > 0
        for error in errors:
            assert error.before_subs == pattern
