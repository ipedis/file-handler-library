import unittest
import os
from unittest.mock import patch, Mock
from file_handler_library.adapter.scaleway_adapter import ScalewayAdapter
from file_handler_library.config import StorageSettings


class TestScalewayFileHandler(unittest.TestCase):
    def setUp(self):
        # Set up your ScalewayFileHandler instance with test credentials
        self.handler = ScalewayAdapter()

    def test_create_and_delete_file(self):
        bucket_name = 'test-bucket'
        remote_file_name = 'test-file.txt'
        local_file_path = 'test-file.txt'

        # Create a mock S3 client for testing
        mock_s3_client = Mock()
        self.handler.s3 = mock_s3_client

        # Mock S3 upload and delete methods
        mock_s3_client.upload_file = Mock()
        mock_s3_client.delete_object = Mock()

        # Test creating a file
        self.handler.create_file(bucket_name, local_file_path, remote_file_name)
        mock_s3_client.upload_file.assert_called_once_with(
            local_file_path, bucket_name, remote_file_name
        )

        # Test deleting a file
        self.handler.delete_file(bucket_name, remote_file_name)
        mock_s3_client.delete_object.assert_called_once_with(
            Bucket=bucket_name, Key=remote_file_name
        )

    # Add more test cases for other methods as needed


if __name__ == '__main__':
    unittest.main()
