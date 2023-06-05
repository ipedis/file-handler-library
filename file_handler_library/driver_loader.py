from cloudstorage import get_driver_by_name

from file_handler_library.config import StorageSettings
from file_handler_library.exception.storage_exception import InvalidStorageTypeException
from file_handler_library.file_storage_type import FileStorageType


class DriverLoader:
    def __init__(self):
        self.settings: StorageSettings = StorageSettings()

    def get_driver(self):
        if not FileStorageType.is_storage_supported(self.settings.storage_type):
            raise InvalidStorageTypeException(f"We do not support {self.settings.storage_type} yet.")

        return get_driver_by_name(self.settings.storage_type)
