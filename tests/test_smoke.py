import os
import sys
from collections import namedtuple
from pathlib import Path
from unittest.mock import patch

import pytest

from rbv import cli

TEST_EXEC_DIR = Path(__file__).parent.parent

dse_rules_file = "examples/dse_rules.yml"
single_rule_filter_action = "examples/single_rule_single_action.yml"
single_rule_filter_action_FALSE = "examples/FALSE_single_rule_single_action.yml"

YAMLConfig = namedtuple("YAMLConfig", "filepath, cdir, expected")
config_files_data = [
    YAMLConfig(dse_rules_file, ".", False),
    YAMLConfig(single_rule_filter_action, ".", True),
    YAMLConfig(single_rule_filter_action, "./rbv", False),
    YAMLConfig(single_rule_filter_action_FALSE, ".", False),
]


@pytest.mark.smoke
@pytest.mark.parametrize(
    "full_path, current_dir, expected",
    config_files_data,
    indirect=["full_path", "current_dir"],
)
def test_expected_output(full_path, current_dir, expected, capsys):
    test_args = ["test", "validate", full_path]
    compare_main_with_expected_output(test_args, expected, capsys)


@pytest.mark.smoke
@pytest.mark.skip(reason="Requires impleming --directory feature")
@pytest.mark.parametrize("filepath, targeted_dir, expected", config_files_data)
def test_expected_output_when_specifying_dir(filepath, targeted_dir, expected, capsys):
    test_args = ["test", "validate", "--directory", targeted_dir, filepath]
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


@pytest.fixture
def current_dir(request):
    # save current directory
    original_dir = Path.cwd()
    requested_dir = Path(request.param)

    os.chdir(requested_dir.as_posix())

    yield

    # revert to original directory at teardown
    os.chdir(original_dir.as_posix())


@pytest.fixture
def full_path(tmp_path, request):
    original_filepath = Path(request.param)
    return (TEST_EXEC_DIR / original_filepath).as_posix()


ScenarioConfig = namedtuple("ScenarioConfig", "filepath, files, expected")
scenarios_data = [
    ScenarioConfig(
        filepath="examples/dse_rules.yml", files=["predictions.csv"], expected=True
    ),
    ScenarioConfig(
        filepath="examples/dse_rules.yml",
        files=["predictions.csv", "other.sh"],
        expected=True,
    ),
    ScenarioConfig(
        filepath="examples/dse_rules.yml",
        files=["subdir/predictions.csv", "other.sh"],
        expected=False,
    ),
    ScenarioConfig(
        filepath="examples/dse_rules.yml", files=["other.sh"], expected=False
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
    test_args = ["test", "validate", full_path]
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
@pytest.mark.parametrize("full_path", ["examples/d3m_ta1.yml"], indirect=True)
def test_d3m_ta1(dirstructure, full_path, expected, capsys):
    test_args = ["test", "validate", full_path]
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
    "path", [dse_rules_file, single_rule_filter_action, single_rule_filter_action_FALSE]
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


@pytest.fixture
def file_from_content(tmp_path, request):
    new_file = tmp_path / "file"
    new_file.write_text(request.param)
    yield new_file
    new_file.unlink()
