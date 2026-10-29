import os
import re
import tempfile
from typing import BinaryIO

import boto3
from botocore.exceptions import ClientError, NoCredentialsError, PartialCredentialsError

from file_handler_library.config import StorageSettings
from file_handler_library.exception.storage_exception import FileNotFoundException
from file_handler_library.handler.file_handler_abstract import FileHandlerAbstract

NOT_FOUND_ERROR_CODES = {'404', 'NoSuchKey', 'NoSuchBucket'}


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

    def create_file(self, container_name: str, file: BinaryIO | str, filename: str, is_public: bool = False):
        self.__ensure_container(container_name)
        extra_args = {'ACL': 'public-read'} if is_public else None
        if isinstance(file, str):
            self.storage.upload_file(file, container_name, filename, ExtraArgs=extra_args)
        else:
            self.storage.upload_fileobj(file, container_name, filename, ExtraArgs=extra_args)
        return True

    def get_file(self, container_name: str, filename: str) -> str:
        """Download the object to a new temporary file and return its path. The caller owns (and deletes) it."""
        if not self.is_exist(container_name, filename):
            raise FileNotFoundException(f"File {filename} not found.")
        fd, local_file_path = tempfile.mkstemp(suffix=os.path.splitext(filename)[1])
        os.close(fd)
        self.get_file_obj(container_name, filename, local_file_path)
        return local_file_path

    def get_file_obj(self, container_name: str, filename: str, local_file_path: str):
        with open(local_file_path, 'wb') as f:
            self.storage.download_fileobj(container_name, filename, f)

    def delete_file(self, container_name: str, filename: str):
        try:
            self.storage.delete_object(Bucket=container_name, Key=filename)
            return True
        except Exception:
            return False

    def is_exist(self, container_name: str, filename: str):
        # head_object reports a missing key (or bucket) as a bare 404 ClientError, not NoSuchKey.
        # check this for more details https://github.com/boto/boto3/issues/2442
        try:
            self.storage.head_object(Bucket=container_name, Key=filename)
            return True
        except ClientError as e:
            if e.response['Error']['Code'] in NOT_FOUND_ERROR_CODES:
                return False
            raise e

    def get_file_link(self, container_name: str, file_path: str) -> str:
        host = (re.sub(r'^https?://', '', self.settings.storage_url) if self.settings.storage_url
                else f's3.{self.settings.storage_region}.amazonaws.com')
        return 'https://{}.{}/{}'.format(container_name, host, file_path)

    def __ensure_container(self, container_name: str) -> str:
        try:
            self.storage.head_bucket(Bucket=container_name)
        except ClientError as e:
            if e.response['Error']['Code'] not in NOT_FOUND_ERROR_CODES:
                raise e
            self.storage.create_bucket(Bucket=container_name)
        return container_name
