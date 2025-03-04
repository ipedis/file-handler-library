from typing import BinaryIO

from file_handler_library.adapter_finder import AdapterFinder
from file_handler_library.config import StorageSettings
from file_handler_library.file_storage_type import FileStorageType


class FileHandler:
    def __init__(self):
        self.settings: StorageSettings = StorageSettings()
        self.adapter = AdapterFinder().get_adapter()

    def create_file(self, container_name: str, file: BinaryIO | str, filename: str, is_public: bool = False):
        try:
            return self.adapter.create_file(container_name, file, filename, is_public)
        except Exception as e:
            print(e)

    def delete_file(self, container_name: str, filename: str):
        try:
            return self.adapter.delete_file(container_name, filename)
        except Exception as e:
            print(e)

    def is_exist(self, container_name: str, filename: str):
        try:
            return self.adapter.is_exist(container_name, filename)
        except Exception as e:
            print(e)

    def is_local_storage(self) -> bool:
        return self.settings.storage_type == FileStorageType.LOCAL.value

    def get_container_name(self, container_name: str) -> str:
        try:
            # local storage is basically copy-paste so we need path.
            if self.is_local_storage():
                return f"{self.settings.local_storage_base}/{container_name}"
            return container_name
        except Exception as e:
            print(e)

    def get_filename(self, container_name: str, filename: str) -> str:
        try:
            # local storage is basically copy-paste so we need path.
            if self.is_local_storage():
                return filename
            return filename
        except Exception as e:
            print(e)
