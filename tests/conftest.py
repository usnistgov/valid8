import pytest


@pytest.fixture
def files(tmp_path):
    real_dir = tmp_path
    fake_file = tmp_path / "fakefile"
    real_file = tmp_path / "realfile"
    real_file.touch()

    return {"real_dir": real_dir, "fake_file": fake_file, "real_file": real_file}
