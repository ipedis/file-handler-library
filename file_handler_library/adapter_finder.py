from file_handler_library.adapter.local_adapter import LocalAdapter
from file_handler_library.adapter.s3_adapter import S3Adapter
from file_handler_library.config import StorageSettings
from file_handler_library.exception.storage_exception import InvalidStorageTypeException
from file_handler_library.file_storage_type import FileStorageType


class AdapterFinder:
    def get_adapter(self):
        settings: StorageSettings = StorageSettings()
        match settings.storage_type:
            case FileStorageType.S3.value:
                return S3Adapter()
            case FileStorageType.LOCAL.value:
                return LocalAdapter()
            # case FileStorageType.MINIO.value:
            #     driver_name = FileStorageType.MINIO.value
            #     key = self.settings.key
            #     secret = self.settings.secret
            case _:
                raise InvalidStorageTypeException(f"We do not support {settings.storage_type} yet.")