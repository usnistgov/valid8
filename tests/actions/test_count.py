import pytest

from valid8.actions.count import count
from valid8.exceptions import UnknownArgument

single_directory = ["real_dir"]
directory_and_file = ["real_dir", "real_file"]
twelve_files = ["real_file"] * 12

context_data_for_count = [
    (single_directory, 1, True),
    (single_directory, 9999, False),
    (directory_and_file, 2, True),
    (directory_and_file, "2", True),
    (directory_and_file, "2+", True),
    (directory_and_file, "0+", True),
    (directory_and_file, "1+", True),
    (directory_and_file, -9, False),
    (directory_and_file, 0, False),
    (directory_and_file, "0", False),
    (directory_and_file, "3", False),
    (directory_and_file, "3+", False),
    (directory_and_file, "4+", False),
    (["fake_file"], 1, False),
    (["fake_file"], 0, True),
    (["fake_file", "real_dir", "real_file"], 2, True),
    (["fake_file", "real_dir", "real_file"], 10, False),
    (["fake_file", "real_dir", "real_file"], "101+", False),
    (["real_file", "real_file"], 2, True),
    (["fake_file", "fake_file"], 1, False),
    (["fake_file", "fake_file"], 0, True),
    (twelve_files, 12, True),
    (twelve_files, 11, False),
    (twelve_files, 13, False),
    (twelve_files, "12+", True),
    (twelve_files, "11+", True),
    (twelve_files, "13+", False),
    ([], 0, True),
    ([], "0+", True),
]


@pytest.fixture(params=context_data_for_count)
def data_for_count(request, files):
    translated_list = [files[e] for e in request.param[0]]
    return translated_list, request.param[1], request.param[2]


def test_count(data_for_count):
    context, n, expected = data_for_count
    output, errors = count(n, context)
    assert output is expected
    assert output or len(errors) != 0


context_data_for_count_improper_format = [("1a"), ("23+3")]


@pytest.mark.parametrize("improper_input", context_data_for_count_improper_format)
def test_count_improper_format(improper_input):
    context, n = ["real_dir"], improper_input
    exception_message = "count() expects and integer or an integer followed by a plus"
    with pytest.raises(UnknownArgument) as excinfo:
        count(n, context)
    assert exception_message in str(excinfo.value)
