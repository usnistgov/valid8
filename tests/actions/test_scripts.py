import pytest

from valid8.actions.scripts import context_variables, single_script, ScriptError

from ..lib import compare_main_with_expected_output, CURRENT_FILE_REL

single_path_single_command = """
- rulename: checks_with_scripts
  filters:
    path: {filename}
  actions:
    scripts: {command}
"""
multi_path_single_command = """
- rulename: checks_with_scripts
  filters:
    path_list:
      - {filename1}
      - {filename2}
  actions:
    scripts: {command}
"""
single_path_multi_command = """
- rulename: checks_with_scripts
  filters:
    path: {filename}
  actions:
    scripts:
      - {command1}
      - {command2}
"""

lscommand = "ls -l ."
lscommand_with_fullpath = "ls -l {FILEPATH}"
lscommand_with_relpath = "ls -l {DIR_PATH}/{FILENAME}"
lscommand_with_unrecognized_relpath = "ls -l {FILENAME}"
lscommand_doesnt_exist = "ls -l doesnotexist"

commands_ok = [lscommand, lscommand_with_fullpath, lscommand_with_relpath]
commands_fail = [lscommand_doesnt_exist, lscommand_with_unrecognized_relpath]

data_ok = [
    single_path_single_command.format(command=command, filename=CURRENT_FILE_REL)
    for command in commands_ok
]
data_fails = [
    single_path_single_command.format(command=command, filename=CURRENT_FILE_REL)
    for command in commands_fail
]

data_multi_single_ok = [
    multi_path_single_command.format(
        command=command, filename1=CURRENT_FILE_REL, filename2=CURRENT_FILE_REL.parent
    )
    for command in commands_ok
]
data_multi_single_fails = [
    multi_path_single_command.format(
        command=command, filename1=CURRENT_FILE_REL, filename2=CURRENT_FILE_REL.parent
    )
    for command in commands_fail
]

data_multi_multi_ok = [
    single_path_multi_command.format(
        command1=command1, command2=command2, filename=CURRENT_FILE_REL
    )
    for command1 in commands_ok
    for command2 in commands_ok
]
data_multi_multi_fails = [
    single_path_multi_command.format(
        command1=command1, command2=command2, filename=CURRENT_FILE_REL
    )
    for command1 in commands_ok + commands_fail
    for command2 in commands_fail
]


@pytest.mark.parametrize("file_from_content", data_ok, indirect=["file_from_content"])
def test_single_command_ok(file_from_content, capsys):
    test_args = ["test", "apply", file_from_content.as_posix()]
    compare_main_with_expected_output(test_args, True, capsys)


@pytest.mark.parametrize(
    "file_from_content", data_fails, indirect=["file_from_content"]
)
def test_single_command_fails(file_from_content, capsys):
    test_args = ["test", "apply", file_from_content.as_posix()]
    compare_main_with_expected_output(test_args, False, capsys)


@pytest.mark.parametrize(
    "file_from_content", data_multi_single_ok, indirect=["file_from_content"]
)
def test_multi_file_single_command_ok(file_from_content, capsys):
    test_args = ["test", "apply", file_from_content.as_posix()]
    compare_main_with_expected_output(test_args, True, capsys)


@pytest.mark.parametrize(
    "file_from_content", data_multi_single_fails, indirect=["file_from_content"]
)
def test_multi_file_single_command_fails(file_from_content, capsys):
    test_args = ["test", "apply", file_from_content.as_posix()]
    compare_main_with_expected_output(test_args, False, capsys)


@pytest.mark.parametrize(
    "file_from_content", data_multi_multi_ok, indirect=["file_from_content"]
)
def test_single_file_multi_command_ok(file_from_content, capsys):
    test_args = ["test", "apply", file_from_content.as_posix()]
    compare_main_with_expected_output(test_args, True, capsys)


@pytest.mark.parametrize(
    "file_from_content", data_multi_multi_fails, indirect=["file_from_content"]
)
def test_single_file_multi_command_fails(file_from_content, capsys):
    test_args = ["test", "apply", file_from_content.as_posix()]
    compare_main_with_expected_output(test_args, False, capsys)


@pytest.mark.parametrize(
    "filepath, e_dirname, e_filename, e_filenamenoext",
    [
        ("hello/", "", "hello", "hello"),
        ("hello/world/", "hello", "world", "world"),
        ("hello/world", "hello", "world", "world"),
        ("hello/world/file.txt", "world", "file.txt", "file"),
        ("hello world/file.txt", "hello world", "file.txt", "file"),
        (
            "hello/file with spaces.txt",
            "hello",
            "file with spaces.txt",
            "file with spaces",
        ),
    ],
)
def test_variable_substitution(filepath, e_dirname, e_filename, e_filenamenoext):
    variables = context_variables(filepath)
    assert variables["DIR_NAME"] == "'" + e_dirname + "'"
    assert variables["FILENAME"] == "'" + e_filename + "'"
    assert variables["FILENAME_NOEXT"] == "'" + e_filenamenoext + "'"


dirstruct_empty = []
dirstruct_simple = ["hello.txt"]
dirstruct_subdir = ["a/hello.txt"]
dirstruct_multi = ["a/hello.txt", "a/b/hello.txt", "a/b/world.txt", "b/hello.txt"]

dirstruct_all = [dirstruct_empty, dirstruct_simple, dirstruct_subdir, dirstruct_multi]

scenarios_independant_of_dir = [
    ([lscommand], True),
    ([lscommand_doesnt_exist], False),
    ([lscommand, lscommand_doesnt_exist], False),
]

scenarios_with_dirstructure = [
    (dirstruct_multi, "fake/path with spaces", [lscommand_with_fullpath], False),
    (dirstruct_multi, "a/hello.txt", [lscommand_with_fullpath], True),
    (dirstruct_multi, "a/hello.txt", [lscommand_with_relpath], True),
    (dirstruct_subdir, "a/hello.txt", [lscommand_with_fullpath], True),
    (dirstruct_subdir, "a/hello.txt", [lscommand_with_relpath], True),
    (dirstruct_simple, "a/hello.txt", [lscommand_with_fullpath], False),
    (dirstruct_simple, "a/hello.txt", [lscommand_with_relpath], False),
]

scenarios_multi_command_using_test_dirstruct = [
    (CURRENT_FILE_REL, commands_ok, True),
    (CURRENT_FILE_REL, commands_fail, False),
    (CURRENT_FILE_REL, commands_ok + commands_fail, False),
]


@pytest.mark.parametrize("commands, expected", scenarios_independant_of_dir)
@pytest.mark.parametrize("dirstructure", dirstruct_all, indirect=["dirstructure"])
@pytest.mark.parametrize("filepath", [CURRENT_FILE_REL, "fake/path with spaces"])
def test_single_script_independant_of_dir(dirstructure, filepath, commands, expected):
    output, errors = single_script(commands, filepath)
    asserts_for_single_script_output(output, errors, expected)


@pytest.mark.parametrize(
    "dirstructure, filepath, commands, expected",
    scenarios_with_dirstructure,
    indirect=["dirstructure"],
)
def test_single_script_with_dirstructure(dirstructure, filepath, commands, expected):
    output, errors = single_script(commands, filepath)
    asserts_for_single_script_output(output, errors, expected)


@pytest.mark.parametrize(
    "filepath, commands, expected", scenarios_multi_command_using_test_dirstruct
)
def test_single_script_multi_command_using_test_dirstruct(filepath, commands, expected):
    output, errors = single_script(commands, filepath)
    asserts_for_single_script_output(output, errors, expected)


def asserts_for_single_script_output(output, errors, expected):
    if expected is True:
        assert output is True
        assert len(errors) == 0
    else:
        assert output is False
        assert len(errors) == 1
        assert type(errors[0]) == ScriptError
