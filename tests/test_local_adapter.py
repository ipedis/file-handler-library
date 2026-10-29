import os

import pytest

from file_handler_library.adapter.local_adapter import LocalAdapter
from file_handler_library.exception.storage_exception import FileNotFoundException, InvalidPathException

CONTAINER = "pdf-uuid/input"
FILENAME = "test-file.txt"


@pytest.fixture
def adapter(storage_env):
    storage_env.setenv("STORAGE_TYPE", "LOCAL")
    return LocalAdapter()


def test_create_file_from_path(adapter, source_file):
    assert adapter.create_file(CONTAINER, str(source_file), FILENAME) is True

    assert adapter.is_exist(CONTAINER, FILENAME)
    with open(adapter.get_file(CONTAINER, FILENAME)) as f:
        assert f.read() == "Hello, world!"
    assert os.stat(adapter.get_file(CONTAINER, FILENAME)).st_mode & 0o777 == 0o664


def test_create_file_from_binary_stream(adapter, source_file):
    with open(source_file, "rb") as stream:
        adapter.create_file(CONTAINER, stream, FILENAME)

    with open(adapter.get_file(CONTAINER, FILENAME)) as f:
        assert f.read() == "Hello, world!"


def test_create_file_raises_when_source_is_missing(adapter, tmp_path):
    with pytest.raises(OSError):
        adapter.create_file(CONTAINER, str(tmp_path / "missing.txt"), FILENAME)


def test_get_file_obj_copies_to_local_path(adapter, source_file, tmp_path):
    adapter.create_file(CONTAINER, str(source_file), FILENAME)
    destination = tmp_path / "downloaded.txt"

    adapter.get_file_obj(CONTAINER, FILENAME, str(destination))

    assert destination.read_text() == "Hello, world!"


def test_delete_file(adapter, source_file):
    adapter.create_file(CONTAINER, str(source_file), FILENAME)

    assert adapter.delete_file(CONTAINER, FILENAME) is True
    assert not adapter.is_exist(CONTAINER, FILENAME)
    # deleting a missing file is not an error
    assert adapter.delete_file(CONTAINER, FILENAME) is True


def test_file_not_found(adapter):
    with pytest.raises(FileNotFoundException):
        adapter.get_file(CONTAINER, "non-existent-file.txt")


@pytest.mark.parametrize("container_name, filename", [
    ("../outside", FILENAME),
    (CONTAINER, "../../../outside.txt"),
    ("/etc", "passwd"),
    (CONTAINER, "/etc/passwd"),
    ("", ""),
])
def test_paths_outside_storage_root_are_rejected(adapter, source_file, container_name, filename):
    with pytest.raises(InvalidPathException):
        adapter.create_file(container_name, str(source_file), filename)
    with pytest.raises(InvalidPathException):
        adapter.is_exist(container_name, filename)
    with pytest.raises(InvalidPathException):
        adapter.get_file(container_name, filename)
    with pytest.raises(InvalidPathException):
        adapter.delete_file(container_name, filename)


def test_symlink_escaping_storage_root_is_rejected(adapter, source_file, tmp_path):
    outside = tmp_path / "outside"
    outside.mkdir()
    os.symlink(outside, os.path.join(adapter.root_dir, "link"))

    with pytest.raises(InvalidPathException):
        adapter.create_file("link", str(source_file), FILENAME)
