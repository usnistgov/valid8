from unittest.mock import patch
from pathlib import Path
import sys

from valid8 import cli

CURRENT_FILE = Path(__file__)
TEST_EXEC_DIR = CURRENT_FILE.parent.parent
CURRENT_FILE_REL = CURRENT_FILE.relative_to(TEST_EXEC_DIR)


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
