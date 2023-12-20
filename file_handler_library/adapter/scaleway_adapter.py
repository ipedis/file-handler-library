from typing import BinaryIO

import boto3
from botocore.exceptions import NoCredentialsError, PartialCredentialsError

from file_handler_library.config import StorageSettings
from file_handler_library.exception.storage_exception import FileNotFoundException
from file_handler_library.handler.file_handler_abstract import FileHandlerAbstract


class ScalewayAdapter(FileHandlerAbstract):
    def __init__(self):
        self.settings: StorageSettings = StorageSettings()
        try:
            self.storage = boto3.client(
                's3',
                aws_access_key_id=self.settings.key,
                aws_secret_access_key=self.settings.secret,
                endpoint_url=self.settings.storage_url,
                region_name=self.settings.storage_region,
            )
        except (NoCredentialsError, PartialCredentialsError) as e:
            raise Exception("Scaleway credentials are invalid. Please check and try again.") from e

    def create_file(self, container_name: str, file: BinaryIO | str, filename: str):
        try:
            self.__get_container(container_name=container_name)
            self.storage.upload_file(file, container_name, filename)
            return True
        except Exception:
            return False

    def get_file(self, container_name: str, filename: str):
        raise NotImplementedError

    def get_file_obj(self, container_name: str, filename: str, local_file_path: str):
        try:
            with open(local_file_path, 'wb') as f:
                self.storage.download_fileobj(container_name, filename, f)
        except Exception as e:
            raise e

    def delete_file(self, container_name: str, filename: str):
        try:
            self.__get_container(container_name=container_name)
            self.storage.delete_object(Bucket=container_name, Key=filename)
            return True
        except Exception:
            return False

    def is_exist(self, container_name: str, filename: str):
        try:
            self.__get_container(container_name=container_name)
            self.storage.head_object(Bucket=container_name, Key=filename)
            return True
        except self.storage.exceptions.NoSuchKey:
            return False

    def __get_container(self, container_name: str) -> str:
        response = self.storage.list_buckets()
        for bucket in response['Buckets']:
            if bucket['Name'] == container_name:
                return container_name
        self.storage.create_bucket(Bucket=container_name)
        return container_name
