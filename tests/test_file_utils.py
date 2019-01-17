from rbv.file_utils import filepath_exists


def asserts_filepath_exists(dirpath):
    assert filepath_exists(dirpath)
    assert filepath_exists(dirpath.as_posix())
    assert not filepath_exists(dirpath / "fakefile")
    assert not filepath_exists((dirpath / "fakefile").as_posix())
    realfile = dirpath / "realfile.txt"
    realfile.touch()
    assert filepath_exists(realfile)
    assert filepath_exists(realfile.as_posix())


def test_filepath_exists(tmp_path):
    asserts_filepath_exists(tmp_path)


def test_pattern_matches():
    pass


def test_pattern_exists():
    pass
