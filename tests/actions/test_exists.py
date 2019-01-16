import pytest

from rbv.actions.exists import _file_exists, exists
from rbv.actions.count import count


def test_file_existence(tmp_path):
    assert _file_exists(tmp_path)
    assert _file_exists(tmp_path.as_posix())
    assert not _file_exists(tmp_path / "fakefile")
    assert not _file_exists((tmp_path / "fakefile").as_posix())
    realfile = tmp_path / "realfile.txt"
    realfile.touch()
    assert _file_exists(realfile)
    assert _file_exists(realfile.as_posix())


context_data_for_exists = [
    (["real_dir"], True),
    (["real_dir", "real_file"], True),
    (["fake_file"], False),
    (["fake_file", "real_dir", "real_file"], False),
    (["fake_file", "fake_file"], False),
    ([], True),
]


@pytest.fixture
def files(tmp_path):
    real_dir = tmp_path
    fake_file = tmp_path / "fakefile"
    real_file = tmp_path / "realfile"
    real_file.touch()

    return {"real_dir": real_dir, "fake_file": fake_file, "real_file": real_file}


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
