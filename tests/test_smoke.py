import os
import sys
from collections import namedtuple
from pathlib import Path
from unittest.mock import patch

import pytest

from rbv import cli

TEST_EXEC_DIR = Path(__file__).parent.parent

YAMLConfig = namedtuple("YAMLConfig", "filepath, cdir, success")
config_files_data = [
    YAMLConfig("examples/dse_rules.yml", ".", False),
    YAMLConfig("examples/single_rule_single_action.yml", ".", True),
    YAMLConfig("examples/single_rule_single_action.yml", "./rbv", False),
    YAMLConfig("examples/FALSE_single_rule_single_action.yml", ".", False),
]


@pytest.fixture(params=config_files_data)
def config_conditions(request):
    # save current directory
    original_dir = Path.cwd()
    original_filepath = Path(request.param.filepath)
    requested_dir = Path(request.param.cdir)

    os.chdir(requested_dir.as_posix())

    yield YAMLConfig(
        filepath=(TEST_EXEC_DIR / original_filepath).as_posix(),
        cdir=requested_dir,
        success=request.param.success,
    )

    # revert to original directory at teardown
    os.chdir(original_dir.as_posix())


@pytest.mark.smoke
def test_expected_output(config_conditions, capsys):
    test_args = ["test", "validate", config_conditions.filepath]
    with patch.object(sys, "argv", test_args):
        try:
            cli.main()
        except SystemExit as sysexit:
            out, err = capsys.readouterr()
            if config_conditions.success is True:
                assert sysexit.code == 0
                assert out.strip().endswith("True")
            else:
                assert sysexit != 0
                assert out.strip().endswith("False")

            assert not out.strip().endswith("sanitycheck")


ScenarioConfig = namedtuple("ScenarioConfig", "filepath, files, success")
scenarios_data = [
    ScenarioConfig(
        filepath="examples/dse_rules.yml", files=["predictions.csv"], success=True
    ),
    ScenarioConfig(
        filepath="examples/dse_rules.yml",
        files=["predictions.csv", "other.sh"],
        success=True,
    ),
    ScenarioConfig(
        filepath="examples/dse_rules.yml",
        files=["subdir/predictions.csv", "other.sh"],
        success=False,
    ),
    ScenarioConfig(
        filepath="examples/dse_rules.yml", files=["other.sh"], success=False
    ),
]


@pytest.fixture(params=scenarios_data)
def scenario_config_conditions(request, tmp_path):
    # save current directory
    original_dir = Path.cwd()
    original_filepath = Path(request.param.filepath)
    requested_dir = tmp_path / "testdir"
    requested_dir.mkdir()
    for f in request.param.files:
        f_path = requested_dir / Path(f)
        f_path.parent.mkdir(parents=True, exist_ok=True)
        f_path.touch()

    # scenario = request.param.copy()
    # scenario.filepath = (TEST_EXEC_DIR / original_filepath).as_posix()

    os.chdir(requested_dir.as_posix())

    yield ScenarioConfig(
        filepath=(TEST_EXEC_DIR / original_filepath).as_posix(),
        files=request.param.files,
        success=request.param.success,
    )

    # revert to original directory at teardown
    os.chdir(original_dir.as_posix())


@pytest.mark.smoke
def test_with_fake_structure(scenario_config_conditions, capsys):
    test_args = ["test", "validate", scenario_config_conditions.filepath]
    with patch.object(sys, "argv", test_args):
        try:
            cli.main()
        except SystemExit as sysexit:
            out, err = capsys.readouterr()
            if scenario_config_conditions.success is True:
                assert sysexit.code == 0
                assert out.strip().endswith("True")
            else:
                assert sysexit != 0
                assert out.strip().endswith("False")

            assert not out.strip().endswith("sanitycheck")
