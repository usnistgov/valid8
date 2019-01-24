from unittest.mock import patch
import sys

from rbv import cli


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
