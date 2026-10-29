import os

import pytest
from moto import mock_aws

from file_handler_library.adapter.scaleway_adapter import ScalewayAdapter
from file_handler_library.exception.storage_exception import FileNotFoundException

BUCKET = "test-bucket"
KEY = "pdf-uuid/input/test-file.txt"


@pytest.fixture
def adapter(storage_env):
    storage_env.setenv("STORAGE_TYPE", "S3")
    with mock_aws():
        yield ScalewayAdapter()


def test_create_file_creates_missing_bucket(adapter, source_file):
    assert adapter.create_file(BUCKET, str(source_file), KEY) is True

    assert adapter.is_exist(BUCKET, KEY)
    assert BUCKET in [b["Name"] for b in adapter.storage.list_buckets()["Buckets"]]


def test_create_file_from_binary_stream(adapter, source_file, tmp_path):
    with open(source_file, "rb") as stream:
        adapter.create_file(BUCKET, stream, KEY)

    destination = tmp_path / "downloaded.txt"
    adapter.get_file_obj(BUCKET, KEY, str(destination))
    assert destination.read_text() == "Hello, world!"


def test_public_file_gets_public_read_acl(adapter, source_file):
    adapter.create_file(BUCKET, str(source_file), KEY, is_public=True)

    grants = adapter.storage.get_object_acl(Bucket=BUCKET, Key=KEY)["Grants"]
    assert any(g["Permission"] == "READ" and g["Grantee"].get("URI", "").endswith("/AllUsers") for g in grants)


def test_get_file_downloads_to_temporary_file(adapter, source_file):
    adapter.create_file(BUCKET, str(source_file), KEY)

    local_path = adapter.get_file(BUCKET, KEY)
    try:
        with open(local_path) as f:
            assert f.read() == "Hello, world!"
        assert not os.path.exists(os.path.basename(KEY))
    finally:
        os.remove(local_path)


def test_get_file_raises_when_missing(adapter, source_file):
    adapter.create_file(BUCKET, str(source_file), KEY)

    with pytest.raises(FileNotFoundException):
        adapter.get_file(BUCKET, "missing.txt")


def test_is_exist_does_not_create_bucket(adapter):
    assert adapter.is_exist(BUCKET, KEY) is False
    assert adapter.storage.list_buckets()["Buckets"] == []


def test_delete_file(adapter, source_file):
    adapter.create_file(BUCKET, str(source_file), KEY)

    assert adapter.delete_file(BUCKET, KEY) is True
    assert adapter.is_exist(BUCKET, KEY) is False


def test_get_file_link_uses_storage_url(storage_env):
    storage_env.setenv("STORAGE_TYPE", "SCALEWAY")
    storage_env.setenv("STORAGE_URL", "https://s3.fr-par.scw.cloud")

    assert ScalewayAdapter().get_file_link(BUCKET, KEY) == f"https://{BUCKET}.s3.fr-par.scw.cloud/{KEY}"


def test_get_file_link_without_storage_url_falls_back_to_aws(adapter):
    assert adapter.get_file_link(BUCKET, KEY) == f"https://{BUCKET}.s3.us-east-1.amazonaws.com/{KEY}"
