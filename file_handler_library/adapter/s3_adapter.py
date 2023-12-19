from typing import BinaryIO

from cloudstorage.exceptions import NotFoundError

from file_handler_library.config import StorageSettings
from file_handler_library.driver_loader import DriverLoader
from file_handler_library.exception.storage_exception import FileNotFoundException
from file_handler_library.file_storage_type import FileStorageType
from file_handler_library.handler.file_handler_abstract import FileHandlerAbstract


class S3Adapter(FileHandlerAbstract):
    def __init__(self):
        self.settings: StorageSettings = StorageSettings()
        self.driver = DriverLoader().get_driver(FileStorageType.S3.value)
        self.storage = self.driver(key=self.settings.key, secret=self.settings.secret, region=self.settings.storage_region)

    def get_file_obj(self, container_name: str, filename: str, local_file_path:str):
        raise NotImplementedError

    def create_file(self, container_name: str, file: BinaryIO | str, filename: str):
        try:
            self.__get_container(container_name).upload_blob(filename=file, blob_name=filename)
            return True
        except Exception as e:
            return False

    def get_file(self, container_name: str, filename: str):
        if self.is_exist(container_name, filename):
            return self.__get_container(container_name).get_blob(blob_name=filename)
        raise FileNotFoundException(f"File {filename} not found.")

    def delete_file(self, container_name: str, filename: str):
        if not self.is_exist(container_name, filename):
            return True
        blob = self.__get_container(container_name).get_blob(blob_name=filename)
        blob.delete()
        return True

    def is_exist(self, container_name: str, filename: str):
        try:
            self.__get_container(container_name).get_blob(blob_name=filename)
            return True
        except NotFoundError or FileNotFoundError:
            return False

    def __get_container(self, container_name: str):
        try:
            return self.storage.get_container(container_name)
        except NotFoundError:
            return self.storage.create_container(container_name=container_name)
