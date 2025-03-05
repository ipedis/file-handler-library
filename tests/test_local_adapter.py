import os
import unittest
import tempfile

from dotenv import load_dotenv

from file_handler_library.adapter.local_adapter import LocalAdapter
from file_handler_library.config import StorageSettings
from file_handler_library.exception.storage_exception import FileNotFoundException


class TestLocalAdapter(unittest.TestCase):
    def setUp(self):
        load_dotenv()
        self.settings = StorageSettings()
        self.adapter = LocalAdapter()

    def tearDown(self):
        # delete all files inside local storage
        for root, dirs, files in os.walk(self.settings.local_storage_base):
            for file in files:
                print(os.path.join(root, file))
                os.remove(os.path.join(root, file))

    def test_create_file(self):
        container_name = "test-container"
        filename = "test-file.txt"
        file_content = "Hello, world!"

        # Create a file
        result = self.adapter.create_file(container_name, file_content, filename)
        self.assertTrue(result)

        # Check if the file exists
        self.assertTrue(self.adapter.is_exist(container_name, filename))

    def test_get_file(self):
        container_name = "test-container"
        filename = "test-file.txt"
        file_content = "Hello, world!"

        # Create a file
        self.adapter.create_file(container_name, file_content, filename)

        # Get the file path
        file_path = self.adapter.get_file(container_name, filename)
        self.assertTrue(os.path.exists(file_path))

    def test_delete_file(self):
        container_name = "test-container"
        filename = "test-file.txt"
        file_content = "Hello, world!"

        # Create a file
        self.adapter.create_file(container_name, file_content, filename)

        # Delete the file
        result = self.adapter.delete_file(container_name, filename)
        self.assertTrue(result)

        # Check if the file exists
        self.assertFalse(self.adapter.is_exist(container_name, filename))

    def test_file_not_found(self):
        container_name = "test-container"
        filename = "non-existent-file.txt"

        with self.assertRaises(FileNotFoundException):
            self.adapter.get_file(container_name, filename)


if __name__ == '__main__':
    unittest.main()
