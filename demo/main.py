import os.path
import uuid

from dotenv import load_dotenv

from demo.file_handler import FileHandler


# this shows the demo of how to use the file_handler_library
def main():
    load_dotenv()
    file_handler = FileHandler()
    container_name = "text"
    filename = f"{uuid.uuid4()}.txt"
    upload_file = "demo/doc/sample.txt"
    # create file
    full_path = os.path.abspath(upload_file)
    if file_handler.is_local_storage():
        with open(full_path, "rb") as file:
            file_handler.create_file(container_name, file, filename)
            file.close()
    else:
        file_handler.create_file(container_name, full_path, filename)
    # check if file exists
    if file_handler.is_exist(container_name, filename):
        print("File uploaded successfully. Now deleting the file.")
        # delete file
        # file_handler.delete_file(container_name, filename)
        # following should print False
        print(f"File deleted. Checking if file exists: {file_handler.is_exist(container_name, filename)}")
    else:
        print("File upload failed.")


if __name__ == "__main__":
    main()
