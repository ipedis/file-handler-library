import os.path

from dotenv import load_dotenv

from file_handler_library.adapter_finder import AdapterFinder



def main():
    load_dotenv()

    # Create an instance of AdapterFinder
    adapter_finder = AdapterFinder()

    # Get the appropriate adapter based on the storage type
    adapter = adapter_finder.get_adapter()

    # Perform some basic operations using the adapter
    container_name = "test-bucket"
    filename = "sample.txt"
    file_content = os.path.abspath('demo/storage/sample.txt')

    # Upload a file
    adapter.create_file(container_name, file_content, filename, is_public=True)
    print(f"File '{filename}' uploaded to '{container_name}'.")

    # Check if the file exists
    if adapter.is_exist(container_name, filename):
        print(f"File '{filename}' exists in '{container_name}'.")

    # Delete the file
    # adapter.delete_file(container_name, filename)
    # print(f"File '{filename}' deleted from '{container_name}'.")


if __name__ == "__main__":
    main()
