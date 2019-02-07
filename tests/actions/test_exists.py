import pytest

from valid8.actions.count import count
from valid8.actions.exists import exists


context_data_for_exists = [
    (["real_dir"], True),
    (["real_dir", "real_file"], True),
    (["fake_file"], False),
    (["fake_file", "real_dir", "real_file"], False),
    (["fake_file", "fake_file"], False),
    ([], True),
]


@pytest.fixture(params=context_data_for_exists)
def data_for_exists(request, files):
    translated_list = [files[e] for e in request.param[0]]
    return translated_list, request.param[1]


@pytest.mark.parametrize("_boolean", (True, False, "optional"))
def test_exists(data_for_exists, _boolean):
    context, expected = data_for_exists
    output, errors = exists(_boolean, context)
    assert output is expected
    assert output or len(errors) != 0


context_data_for_count = [
    (["real_dir"], 1, True),
    (["real_dir"], 9999, False),
    (["real_dir", "real_file"], 2, True),
    (["real_dir", "real_file"], -9, False),
    (["real_dir", "real_file"], 0, False),
    (["fake_file"], 1, False),
    (["fake_file"], 0, True),
    (["fake_file", "real_dir", "real_file"], 2, True),
    (["fake_file", "fake_file"], 1, False),
    (["fake_file", "fake_file"], 0, True),
    ([], 0, True),
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
