import pytest

from valid8.actions.count import count


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
