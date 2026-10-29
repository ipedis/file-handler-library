# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Project

`file-handler-library` is a small Python library (Python >= 3.11, managed with uv, built with hatchling) that gives consuming projects one storage API over local disk and S3-compatible object stores (AWS S3, Scaleway, MinIO). Only the `file_handler_library/` package is shipped; `demo/` and `tests/` are not.

It is consumed as a git dependency pinned to a tag (`rev = "vX.Y.Z"`) by the sibling Poetry projects in `../` (pdf-json-api, pdf-orchestrator, pdf-pretreatment, pdf-sdk-api, pdf-tagging-api). Consumers never see `uv.lock`: only `[project].dependencies` and `requires-python` matter to them, so keep dependency bounds loose (minimums only) and bump the major version for behaviour changes. Those projects call `create_file` with a file path and use `<uuid>/<step>` sub-directories as local container names.

## Commands

```bash
uv sync                                                    # install deps (incl. dev group)
uv run pytest                                              # all tests
uv run pytest tests/test_local_adapter.py::test_delete_file   # single test
uv run pip-audit                                           # vulnerability audit
docker compose up --build                                  # demo against a moto S3 server
```

There is no linter or formatter configured.

## Architecture

- `config.StorageSettings` (pydantic-settings) is the only source of configuration: env vars, then a `.env` file **relative to the current working directory**. Required: `STORAGE_TYPE`, `KEY`, `SECRET`, `APP_ENV`. Optional: `STORAGE_URL`, `STORAGE_REGION`, `LOCAL_STORAGE_BASE`. Every adapter instantiates its own `StorageSettings()` in `__init__`, so env must be set before construction.
- `adapter_finder.AdapterFinder.get_adapter()` maps `STORAGE_TYPE` (`file_storage_type.FileStorageType`) to an adapter: `LOCAL` -> `LocalAdapter`; `S3`, `SCALEWAY`, `MINIO` -> `ScalewayAdapter` (generic boto3 S3 client, `STORAGE_URL` as `endpoint_url`). Consumers also instantiate `LocalAdapter()` directly as a scratch handler alongside the S3 one.
- `handler.file_handler_abstract.FileHandlerAbstract` is the contract. A "container" is a bucket for S3 and a sub-directory of `LOCAL_STORAGE_BASE` for local. `create_file` accepts a source file path or a binary stream and raises on failure; `get_file` returns a local path (the stored file for local, a temp copy for S3).
- `LocalAdapter.__resolve_path` is the single place that builds file paths; it rejects anything resolving outside the storage root (`InvalidPathException`). Route every new local file operation through it.
- `ScalewayAdapter`: only `create_file` creates a missing bucket. Not-found checks accept `404`, `NoSuchKey` and `NoSuchBucket` because `head_object` reports a bare 404 (boto/boto3#2442).

## Tests

`tests/conftest.py` isolates every test: `storage_env` chdirs into `tmp_path` (so no `.env` is picked up), sets the env vars and points `LOCAL_STORAGE_BASE` at a temp dir. S3 tests run against `moto.mock_aws()`.
