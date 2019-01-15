import pytest

from rbv import cli


@pytest.fixture(scope="module")
def parser():
    return cli.define_cli()


# test that incorrect args raise Exception
incorrect_args_data = [["wrongArgument"], [""]]


# TODO the asserts here are not working
@pytest.mark.parametrize("cli_args", incorrect_args_data)
def test_incorrect_args(cli_args, parser):
    with pytest.raises(SystemExit) as sysexit:
        parser.parse_args(cli_args)
        print(sysexit, sysexit.value)
        assert sysexit.code is not None and sysexit != 0

        # captured = capsys.readouterr()
        # assert captured.startswith('Zusage')


mapping_func_data = [
    (["validate", "something"], cli.cmd_run_validation),
    (["lint", "something"], cli.cmd_run_lint),
]


# test that checks that args call the correct func
@pytest.mark.parametrize("cli_args, expected_func", mapping_func_data)
def test_mapping_func(parser, cli_args, expected_func):
    args = parser.parse_args(cli_args)
    assert callable(args.func)
    assert args.func == expected_func
