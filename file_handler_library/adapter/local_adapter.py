import os
import shutil
from typing import BinaryIO


from file_handler_library.config import StorageSettings
from file_handler_library.exception.storage_exception import FileNotFoundException, NotADirectoryException, \
    InvalidStorageTypeException
from file_handler_library.file_storage_type import FileStorageType
from file_handler_library.handler.file_handler_abstract import FileHandlerAbstract


class LocalAdapter(FileHandlerAbstract):
    def __init__(self):
        self.settings: StorageSettings = StorageSettings()
        self.root_dir = self.settings.local_storage_base
        if (self.root_dir is None or self.root_dir == "") and FileStorageType.LOCAL.value == self.settings.storage_type:
            raise InvalidStorageTypeException(message="Please set local storage base path.")
        try:
            if not os.path.exists(self.root_dir):
                os.makedirs(self.root_dir)
        except PermissionError as e:
            raise e
        if not os.path.isdir(self.root_dir):
            raise NotADirectoryException(message=f"Given path {self.root_dir} is not a directory.")

    def get_file_obj(self, container_name: str, filename: str, local_file_path: str):
        remote_file_path = self.get_file(container_name, filename)
        shutil.copyfile(remote_file_path, local_file_path)

    def create_file(self, container_name: str, file: str, filename: str, is_public: bool = False):
        try:
            # create directory
            self.__get_container(container_name)

            file_path = f"{self.root_dir}/{container_name}/{filename}"
            with open(file_path, "w") as storage_file:
                print(file, file=storage_file)
            # Disable execute mode on file
            os.chmod(file_path, int("664", 8))
            return True
        except Exception as e:
            print(e)
            return e

    def get_file(self, container_name: str, filename: str) -> str:
        if self.is_exist(container_name, filename):
            return f"{self.__get_container(container_name)}/{filename}"
        raise FileNotFoundException(f"File {filename} not found.")

    def delete_file(self, container_name: str, filename: str):
        if not self.is_exist(container_name, filename):
            return True
        os.remove(f"{self.__get_container(container_name)}/{filename}")
        return True

    def is_exist(self, container_name: str, filename: str):
        return os.path.exists(f"{self.__get_container(container_name)}/{filename}")

    def get_file_link(self, container_name: str, file_path: str) -> str:
        return file_path

    def __get_container(self, container_name: str):
        full_path = os.path.join(self.root_dir, container_name)
        if not os.path.exists(full_path):
            try:
                os.makedirs(full_path)
            except OSError as e:
                raise e
        return full_path
