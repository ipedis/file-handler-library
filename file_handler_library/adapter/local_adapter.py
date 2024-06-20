import os
import shutil
from typing import BinaryIO

from cloudstorage import Blob
from cloudstorage.exceptions import NotFoundError

from file_handler_library.config import StorageSettings
from file_handler_library.driver_loader import DriverLoader
from file_handler_library.exception.storage_exception import FileNotFoundException
from file_handler_library.file_storage_type import FileStorageType
from file_handler_library.handler.file_handler_abstract import FileHandlerAbstract


class LocalAdapter(FileHandlerAbstract):
    def __init__(self):
        self.settings: StorageSettings = StorageSettings()
        self.driver = DriverLoader().get_driver(FileStorageType.LOCAL.value)
        self.storage = self.driver(key=self.settings.local_storage_base, secret=self.settings.secret)

    def get_file_obj(self, container_name: str, filename: str, local_file_path: str):
        remote_file_path = self.get_file(container_name, filename)
        shutil.copyfile(remote_file_path, local_file_path)

    def create_file(self, container_name: str, file: BinaryIO | str, filename: str, is_public: bool = False):
        try:
            if isinstance(file, str):
                # create directory
                self.__get_container(container_name)

                file_path = f"{self.storage.base_path}/{container_name}/{filename}"
                with open(file_path, "w") as blob_file:
                    print(file, file=blob_file)
                # Disable execute mode on file
                os.chmod(file_path, int("664", 8))
            else:
                self.__get_container(container_name).upload_blob(filename=file, blob_name=filename)
            return True
        except Exception as e:
            return False

    def get_file(self, container_name: str, filename: str) -> str | Blob:
        if self.is_exist(container_name, filename):
            blob = self.__get_container(container_name).get_blob(blob_name=filename)
            return f"{self.storage.base_path}/{blob.path}"
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

    def get_file_link(self, container_name: str, file_path: str) -> str:
        raise NotImplementedError

    def __get_container(self, container_name: str):
        try:
            return self.storage.get_container(container_name)
        except NotFoundError:
            return self.storage.create_container(container_name=container_name)
