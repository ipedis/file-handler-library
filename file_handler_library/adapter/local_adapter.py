import os
import shutil
from typing import BinaryIO

from file_handler_library.config import StorageSettings
from file_handler_library.exception.storage_exception import FileNotFoundException, NotADirectoryException, \
    InvalidStorageTypeException, InvalidPathException
from file_handler_library.file_storage_type import FileStorageType
from file_handler_library.handler.file_handler_abstract import FileHandlerAbstract


class LocalAdapter(FileHandlerAbstract):
    def __init__(self):
        self.settings: StorageSettings = StorageSettings()
        self.root_dir = self.settings.local_storage_base
        if (self.root_dir is None or self.root_dir == "") and FileStorageType.LOCAL.value == self.settings.storage_type:
            raise InvalidStorageTypeException(message="Please set local storage base path.")
        if not os.path.exists(self.root_dir):
            os.makedirs(self.root_dir)
        if not os.path.isdir(self.root_dir):
            raise NotADirectoryException(message=f"Given path {self.root_dir} is not a directory.")

    def get_file_obj(self, container_name: str, filename: str, local_file_path: str):
        remote_file_path = self.get_file(container_name, filename)
        shutil.copyfile(remote_file_path, local_file_path)

    def create_file(self, container_name: str, file: BinaryIO | str, filename: str, is_public: bool = False):
        file_path = self.__resolve_path(container_name, filename)
        os.makedirs(os.path.dirname(file_path), exist_ok=True)
        if isinstance(file, str):
            shutil.copyfile(file, file_path)
        else:
            with open(file_path, "wb") as storage_file:
                shutil.copyfileobj(file, storage_file)
        # Disable execute mode on file
        os.chmod(file_path, 0o664)
        return True

    def get_file(self, container_name: str, filename: str) -> str:
        file_path = self.__resolve_path(container_name, filename)
        if os.path.isfile(file_path):
            return file_path
        raise FileNotFoundException(f"File {filename} not found.")

    def delete_file(self, container_name: str, filename: str):
        file_path = self.__resolve_path(container_name, filename)
        if os.path.isfile(file_path):
            os.remove(file_path)
        return True

    def is_exist(self, container_name: str, filename: str):
        return os.path.isfile(self.__resolve_path(container_name, filename))

    def get_file_link(self, container_name: str, file_path: str) -> str:
        return file_path

    def __resolve_path(self, container_name: str, filename: str) -> str:
        """Build the absolute path of a stored file, refusing anything that escapes the storage root
        (``..`` segments, absolute paths, symlinks pointing outside)."""
        root = os.path.realpath(self.root_dir)
        file_path = os.path.realpath(os.path.join(root, container_name, filename))
        if file_path == root or os.path.commonpath([root, file_path]) != root:
            raise InvalidPathException(f"Path {container_name}/{filename} is outside of the storage root.")
        return file_path
