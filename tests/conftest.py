import os
from pathlib import Path

import pytest

TEST_EXEC_DIR = Path(__file__).parent.parent


@pytest.fixture
def files(tmp_path):
    real_dir = tmp_path
    fake_file = tmp_path / "fakefile"
    real_file = tmp_path / "realfile"
    real_file.touch()

    return {"real_dir": real_dir, "fake_file": fake_file, "real_file": real_file}


@pytest.fixture
def dirstructure(tmp_path, request):
    original_dir = Path.cwd()

    for f in request.param:
        f_path = tmp_path / Path(f)
        f_path.parent.mkdir(parents=True, exist_ok=True)
        f_path.touch()

    os.chdir(tmp_path)

    yield request.param

    os.chdir(original_dir.as_posix())


@pytest.fixture
def current_dir(request):
    # save current directory
    original_dir = Path.cwd()
    requested_dir = Path(request.param)

    os.chdir(requested_dir.as_posix())

    yield

    # revert to original directory at teardown
    os.chdir(original_dir.as_posix())


@pytest.fixture
def full_path(tmp_path, request):
    original_filepath = Path(request.param)
    return (TEST_EXEC_DIR / original_filepath).as_posix()


@pytest.fixture
def file_from_content(tmp_path, request):
    new_file = tmp_path / "file"
    new_file.write_text(request.param)
    yield new_file
    new_file.unlink()
