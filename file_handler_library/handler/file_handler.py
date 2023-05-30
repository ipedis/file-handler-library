from typing import BinaryIO

from file_handler_library.handler.file_handler_abstract import FileHandlerAbstract


class FileHandler(FileHandlerAbstract):
    def create_file(self, pdf_id: int, pdf: BinaryIO):
        pass

    def delete_file(self):
        pass

    def create_dir(self):
        pass

    def delete_dir(self):
        pass

    def list_contents(self):
        pass

    def is_dir_empty(self):
        pass

    def is_exist(self):
        pass

    def is_file(self):
        pass

    def is_dir(self):
        pass