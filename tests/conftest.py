import pytest

STORAGE_ENV = {
    "KEY": "testing",
    "SECRET": "testing",
    "APP_ENV": "test",
    "STORAGE_REGION": "us-east-1",
}


@pytest.fixture
def storage_env(monkeypatch, tmp_path):
    """Isolate StorageSettings from any .env file and point local storage at a temporary directory."""
    monkeypatch.chdir(tmp_path)
    for name, value in STORAGE_ENV.items():
        monkeypatch.setenv(name, value)
    monkeypatch.setenv("LOCAL_STORAGE_BASE", str(tmp_path / "storage"))
    return monkeypatch


@pytest.fixture
def source_file(tmp_path):
    path = tmp_path / "source.txt"
    path.write_text("Hello, world!")
    return path
