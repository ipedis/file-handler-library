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
    # def __load_driver(self):
    #     match self.settings.storage_type:
    #         case FileStorageType.S3.value:
    #             driver_name = FileStorageType.S3.value
    #             key = self.settings.key
    #             secret = self.settings.secret
    #         case FileStorageType.LOCAL.value:
    #             driver_name = FileStorageType.LOCAL.value
    #             # for local storage , key is the path to local storage directory
    #             key = self.settings.key
    #             secret = self.settings.secret
    #         case FileStorageType.MINIO.value:
    #             driver_name = FileStorageType.MINIO.value
    #             key = self.settings.key
    #             secret = self.settings.secret
    #         case _:
    #             raise InvalidStorageTypeException(f"We do not support {self.settings.storage_type} yet.")
    #     driver = get_driver_by_name(driver_name)
    #     return driver(key=key, secret=secret)





