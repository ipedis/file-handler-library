import os

from file_handler_library.config import StorageSettings


class TestLocalAdapter:
    def test_upload_file(self):
        storage_dir = os.getcwd() + '/tests/storage/pdf'
        settings = StorageSettings(
            storage_type='LOCAL',
            key='LOCAL',
            secret='local-test-secret',
            app_env='test',
            storage_url=None
        )