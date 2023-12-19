from enum import Enum


class FileStorageType(Enum):
    LOCAL = 'LOCAL'
    S3 = 'S3'
    MINIO = 'MINIO'
    SCALEWAY = 'SCALEWAY'

    @classmethod
    def is_storage_supported(cls, value):
        return value in cls._member_names_
