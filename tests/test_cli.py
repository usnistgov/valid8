import pytest

from valid8 import cli


@pytest.fixture(scope="module")
def parser():
    return cli.define_parser()


incorrect_args_data = [["wrongArgument"], [""]]


def print_usage_asserts(error_code, stderr):
    assert error_code is not None and error_code != 0
    assert stderr.startswith("usage")


@pytest.mark.parametrize("cli_args", incorrect_args_data)
def test_incorrect_args(cli_args, parser, capsys):
    with pytest.raises(SystemExit) as sysexit:
        parser.parse_args(cli_args)
    print_usage_asserts(error_code=sysexit.value.code, stderr=capsys.readouterr()[1])


mapping_func_data = [
    (["apply", "something"], cli.cmd_run_validation),
    (["lint", "something"], cli.cmd_run_lint),
]


# test that checks that args call the correct func
@pytest.mark.parametrize("cli_args, expected_func", mapping_func_data)
def test_mapping_func(parser, cli_args, expected_func):
    args = parser.parse_args(cli_args)
    assert callable(args.func)
    assert args.func == expected_func
