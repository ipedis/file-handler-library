from typing import BinaryIO

from cloudstorage import Blob
from cloudstorage.exceptions import NotFoundError

from file_handler_library.config import StorageSettings
from file_handler_library.driver_loader import DriverLoader
from file_handler_library.exception.storage_exception import FileNotFoundException, InvalidStorageTypeException
from file_handler_library.handler.file_handler_abstract import FileHandlerAbstract


class MinioAdapter(FileHandlerAbstract):
    def __init__(self):
        self.settings: StorageSettings = StorageSettings()
        # hack to allow minio only in dev mode. On prod or staging it must be "local" or "s3".
        if self.settings.app_env != 'dev':
            raise InvalidStorageTypeException("Minio should only be used in dev mode.")
        self.driver = DriverLoader().get_driver()
        self.storage = self.driver(endpoint="127.0.0.1:9000", key=self.settings.key, secret=self.settings.secret, region='us-east-1', secure=False)

    def create_file(self, container_name: str, file: BinaryIO | str, filename: str):
        try:
            self.__get_container(container_name).upload_blob(filename=file, blob_name=filename)
            return True
        except Exception as e:
            return False

    def get_file(self, container_name: str, filename: str) -> str | Blob:
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
