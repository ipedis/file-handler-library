# file-handler-library

One storage API (`create_file`, `get_file`, `get_file_obj`, `is_exist`, `delete_file`, `get_file_link`) over local disk and S3-compatible object storage (AWS S3, Scaleway, MinIO).

## Installation

Requires Python >= 3.11. Add it as a git dependency of your project:

```toml
# Poetry
file-handler-library = {git = "git@github.com:ipedis/file-handler-library.git", rev = "v2.0.0"}
```

```bash
# uv
uv add "file-handler-library @ git+ssh://git@github.com/ipedis/file-handler-library.git@v2.0.0"
```

## Setup

Configuration is read from environment variables, or from a `.env` file in the current working directory.

```dotenv
# For local storage
STORAGE_TYPE=LOCAL
LOCAL_STORAGE_BASE=./storage/pdf
KEY=key
SECRET=keySecret
APP_ENV=dev

# For S3 / Scaleway / MinIO storage
STORAGE_TYPE=S3            # or SCALEWAY, MINIO
KEY=accessKey
SECRET=secretKey
APP_ENV=dev
STORAGE_URL=https://s3.fr-par.scw.cloud   # endpoint, optional for AWS S3
STORAGE_REGION=fr-par
```

```python
from file_handler_library.adapter_finder import AdapterFinder

storage = AdapterFinder().get_adapter()
storage.create_file("my-container", "/tmp/report.pdf", "reports/report.pdf")
```

## Development

The project is managed with [uv](https://docs.astral.sh/uv/).

```bash
uv sync                  # create .venv and install all dependencies
uv run pytest            # run the tests (local adapter + S3 adapter mocked with moto)
uv run pip-audit         # check dependencies for known vulnerabilities
```

### Demo

`docker compose up --build` starts an S3-compatible server ([moto](https://github.com/getmoto/moto)) and runs `demo/main.py` against it, using `demo/.env`.

## Migrating from v1 to v2

- Python >= 3.11 is required: set `python = ">=3.11,..."` in the consuming project.
- `LocalAdapter.create_file` copies the given source file (path or binary stream). In v1.0.1 it wrote the path string itself into the stored file.
- `create_file` raises on failure for every adapter. `LocalAdapter` used to print the error and return the exception object (which evaluated as true).
- `LocalAdapter` raises `InvalidPathException` when `container_name`/`filename` resolve outside `LOCAL_STORAGE_BASE` (`..`, absolute paths, symlinks). Sub-directories such as `<uuid>/input` are still allowed.
- `LocalAdapter.get_file` returns an absolute path. `is_exist`, `get_file` and `delete_file` no longer create the container directory.
- `ScalewayAdapter.get_file` downloads to a new temporary file and returns its path (the caller deletes it). It used to download into the current directory under the object key and return `None`. It raises `FileNotFoundException` when the object does not exist.
- `ScalewayAdapter.is_exist` and `get_file` no longer list or create buckets. Only `create_file` creates a missing bucket, via `head_bucket` instead of `list_buckets`.
- `create_file` accepts a binary stream on S3 too (`upload_fileobj`).
- `STORAGE_URL` and `STORAGE_REGION` are optional.
- The library no longer installs `pytest`, `pytest-env`, `poetry-audit-plugin`, `filelock`, `itsdangerous` or `xattr`. If a project used one of them, it must declare it itself.
