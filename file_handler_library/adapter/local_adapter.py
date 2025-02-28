import os
import shutil
from typing import BinaryIO


from file_handler_library.config import StorageSettings
from file_handler_library.exception.storage_exception import FileNotFoundException, NotADirectoryException
from file_handler_library.handler.file_handler_abstract import FileHandlerAbstract


class LocalAdapter(FileHandlerAbstract):
    def __init__(self):
        self.settings: StorageSettings = StorageSettings()
        self.root_dir = self.settings.local_storage_base
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

    def create_file(self, container_name: str, file: BinaryIO | str, filename: str, is_public: bool = False):
        try:
            if isinstance(file, str):
                # create directory
                self.__get_container(container_name)

                file_path = f"{self.storage.root_dir}/{container_name}/{filename}"
                with open(file_path, "w") as blob_file:
                    print(file, file=blob_file)
                # Disable execute mode on file
                os.chmod(file_path, int("664", 8))
            else:
                self.__get_container(container_name).upload_blob(filename=file, blob_name=filename)
            return True
        except Exception as e:
            return e

    def get_file(self, container_name: str, filename: str) -> str:
        if self.is_exist(container_name, filename):
            blob = self.__get_container(container_name).get_blob(blob_name=filename)
            return f"{self.storage.root_dir}/{blob.path}"
        raise FileNotFoundException(f"File {filename} not found.")

    def delete_file(self, container_name: str, filename: str):
        if not self.is_exist(container_name, filename):
            return True
        blob = self.__get_container(container_name).get_blob(blob_name=filename)
        blob.delete()
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
