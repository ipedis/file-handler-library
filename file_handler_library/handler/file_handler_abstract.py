from abc import ABC, abstractmethod
from typing import BinaryIO

from cloudstorage import Blob


class FileHandlerAbstract(ABC):
    @abstractmethod
    def create_file(self, container_name: str, file: BinaryIO | str, filename: str):
        raise NotImplementedError

    @abstractmethod
    def delete_file(self, container_name: str, filename: str):
        raise NotImplementedError

    @abstractmethod
    def is_exist(self, container_name: str, filename: str):
        raise NotImplementedError

    @abstractmethod
    def get_file(self, container_name: str, filename: str) -> str | Blob:
        raise NotImplementedError

    @abstractmethod
    def get_file_obj(self, container_name: str, filename: str, local_file_path:str):
        raise NotImplementedError
