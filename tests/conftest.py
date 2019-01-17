import os
from pathlib import Path

import pytest


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
