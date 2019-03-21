import os
import sys
from collections import namedtuple
from pathlib import Path
from unittest.mock import patch

import pytest

from valid8 import cli


dse_rules_file = "tests/data/examples/dse_rules.yml"
single_rule_filter_action = "tests/data/examples/single_rule_single_action.yml"
single_rule_filter_action_false = (
    "tests/data/examples/FALSE_single_rule_single_action.yml"
)

YAMLConfig = namedtuple("YAMLConfig", "filepath, cdir, expected")
config_files_data = [
    YAMLConfig(dse_rules_file, ".", False),
    YAMLConfig(single_rule_filter_action, ".", True),
    YAMLConfig(single_rule_filter_action, "./valid8", False),
    YAMLConfig(single_rule_filter_action_false, ".", False),
]


@pytest.mark.smoke
@pytest.mark.parametrize(
    "full_path, current_dir, expected",
    config_files_data,
    indirect=["full_path", "current_dir"],
)
def test_expected_output(full_path, current_dir, expected, capsys):
    test_args = ["test", "apply", full_path]
    compare_main_with_expected_output(test_args, expected, capsys)


@pytest.mark.smoke
@pytest.mark.parametrize("filepath, targeted_dir, expected", config_files_data)
def test_expected_output_when_specifying_dir(filepath, targeted_dir, expected, capsys):
    test_args = ["test", "apply", "--directory", targeted_dir, filepath]
    compare_main_with_expected_output(test_args, expected, capsys)


file_exists_rule = """
- rulename: checks_in_subdir
  filters:
    path: {filename}
  actions:
    exists: true
"""
filename_exists_data = [
    (file_exists_rule.format(filename="somethingrandom"), ".", False),
    (file_exists_rule.format(filename=Path(__file__).name), ".", False),
    (
        file_exists_rule.format(filename=Path(__file__).name),
        Path(__file__).parent.as_posix(),
        True,
    ),
]


@pytest.mark.parametrize(
    "file_from_content, targeted_dir, expected",
    filename_exists_data,
    indirect=["file_from_content"],
)
def test_specifying_dir_with_rule_filename_exists(
    file_from_content, targeted_dir, expected, capsys
):
    test_args = [
        "test",
        "apply",
        "--directory",
        targeted_dir,
        file_from_content.as_posix(),
    ]
    compare_main_with_expected_output(test_args, expected, capsys)


def compare_main_with_expected_output(test_args, expected, capsys):
    with patch.object(sys, "argv", test_args):
        try:
            cli.main()
        except SystemExit as sysexit:
            out, err = capsys.readouterr()
            if expected is True:
                assert sysexit.code == 0
                assert out.strip().endswith("True")
            else:
                assert sysexit != 0
                assert out.strip().endswith("False")


ScenarioConfig = namedtuple("ScenarioConfig", "filepath, files, expected")
scenarios_data = [
    ScenarioConfig(
        filepath="tests/data/examples/dse_rules.yml",
        files=["predictions.csv"],
        expected=True,
    ),
    ScenarioConfig(
        filepath="tests/data/examples/dse_rules.yml",
        files=["predictions.csv", "other.sh"],
        expected=True,
    ),
    ScenarioConfig(
        filepath="tests/data/examples/dse_rules.yml",
        files=["subdir/predictions.csv", "other.sh"],
        expected=False,
    ),
    ScenarioConfig(
        filepath="tests/data/examples/dse_rules.yml", files=["other.sh"], expected=False
    ),
]


@pytest.fixture
def dir_structure(request, tmp_path):
    # save current directory
    original_dir = Path.cwd()
    requested_dir = tmp_path / "testdir"
    requested_dir.mkdir()
    for f in request.param:
        f_path = requested_dir / Path(f)
        f_path.parent.mkdir(parents=True, exist_ok=True)
        f_path.touch()

    os.chdir(requested_dir.as_posix())

    yield

    # revert to original directory at teardown
    os.chdir(original_dir.as_posix())


@pytest.mark.smoke
@pytest.mark.parametrize(
    "full_path, dir_structure, expected",
    scenarios_data,
    indirect=["full_path", "dir_structure"],
)
def test_with_fake_structure(full_path, dir_structure, expected, capsys):
    test_args = ["test", "apply", full_path]
    compare_main_with_expected_output(test_args, expected, capsys)


ds_single_pipeline = [
    "metadata.yml",
    "predictions/pipelineID/predictions.csv",
    "pipelines/pipelineID.json",
    "executables/pipelineID.sh",
]
ds_sp_extra_predictions = ds_single_pipeline + ["pipelines/other_pipelineID.json"]
ds_sp_missing_exec = ds_single_pipeline[:-1]
ds_sp_extra_exec = ds_single_pipeline + ["executables/pipelineID"]


@pytest.mark.parametrize(
    "dirstructure, expected",
    [
        (ds_single_pipeline, True),
        (ds_sp_extra_predictions, False),
        (ds_sp_missing_exec, False),
        (ds_sp_extra_exec, False),
    ],
    indirect=["dirstructure"],
)
@pytest.mark.parametrize(
    "full_path", ["tests/data/examples/d3m_ta1.yml"], indirect=True
)
def test_d3m_ta1(dirstructure, full_path, expected, capsys):
    test_args = ["test", "apply", full_path]
    compare_main_with_expected_output(test_args, expected, capsys)


correct_rule = """
- rulename: predictions_file
  filters:
    path: predictions.csv
  actions:
    exists: true
"""
missing_filters = """
- rulename: somerulename
  actions:
    exists: true
"""
missing_actions = """
- rulename: somerulename
  filters:
    path: hello.txt
"""
not_a_yml_list = """
somekey: somevalue
"""
wrong_indentation = """
- rulename: somerulename
    filters:
        path: hello.txt
    actions:
        exists: True
"""
unknown_action = """
- rulename: somerulename
  filters:
    path: predictions.csv
  actions:
    fantasyAction: arg1
"""
incorrect_root_key = """
- wrongrootkey: somerulename
  filters:
    path: predictions.csv
  actions:
    exists: true
"""
linter_data = [(correct_rule, True)] + [
    (content, False)
    for content in ["", missing_actions, missing_filters, not_a_yml_list]
]
linter_data_incorrect = {"missing_actions": missing_actions}


@pytest.mark.parametrize(
    "path", [dse_rules_file, single_rule_filter_action, single_rule_filter_action_false]
)
def test_lint_ok(path, capsys):
    test_args = ["test", "lint", path]
    with patch.object(sys, "argv", test_args):
        try:
            cli.main()
        except SystemExit:
            pytest.fail("SystemExit was raised when linting a correct file")
        out, err = capsys.readouterr()
        assert "good" in out


@pytest.mark.parametrize("file_from_content", [correct_rule], indirect=True)
def test_lint_ok_from_content(file_from_content, capsys):
    test_args = ["test", "lint", file_from_content.as_posix()]
    with patch.object(sys, "argv", test_args):
        try:
            cli.main()
        except SystemExit:
            pytest.fail("SystemExit was raised when linting a correct file")
        out, err = capsys.readouterr()
        assert "good" in out


@pytest.mark.parametrize(
    "file_from_content",
    [
        missing_actions,
        missing_filters,
        not_a_yml_list,
        wrong_indentation,
        unknown_action,
        incorrect_root_key,
    ],
    indirect=True,
)
def test_lint_fails_from_content(file_from_content, capsys):
    test_args = ["test", "lint", file_from_content.as_posix()]
    with patch.object(sys, "argv", test_args):
        with pytest.raises(SystemExit) as sysexit:
            cli.main()
        exit_code = sysexit.value.code
        assert exit_code == 2
        out, err = capsys.readouterr()
        assert len(out) != 0


@pytest.mark.smoke
def test_shows_help(capsys):
    test_args = ["valid8"]
    with patch.object(sys, "argv", test_args):
        try:
            cli.main()
        except SystemExit:
            pass
        out, err = capsys.readouterr()
        assert out.startswith("usage") or err.startswith("usage")
