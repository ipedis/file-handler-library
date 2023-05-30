from abc import ABC, abstractmethod
from typing import BinaryIO


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
    def get_file(self, container_name: str, filename: str):
        raise NotImplementedError
