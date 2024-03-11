import os
import shutil
from datetime import datetime


def synchronize_folders(source_folder, destination_folder):
    # Get the list of files in the source and destination folders
    source_files = set(os.listdir(source_folder))
    destination_files = set(os.listdir(destination_folder))

    # Find files that are missing or outdated in the destination folder
    source_files_to_copy = source_files.difference(destination_files)
    dest_files_to_copy = destination_files.difference(source_files)

    # Copy missing or updated files from the source to the destination folder
    for file_name in source_files_to_copy:
        source_file_path = os.path.join(source_folder, file_name)
        # modified
        source_ts = os.path.getmtime(source_file_path)
        source_modified = datetime.fromtimestamp(source_ts).strftime('%Y-%m-%d %H:%M:%S')
        destination_file_path = os.path.join(destination_folder, file_name)
        shutil.copy2(source_file_path, destination_file_path)
        print(f"Copied '{file_name}' to '{destination_folder}'")

    print("Synchronization complete.")


if __name__ == "__main__":
    # Example usage:
    source_folder = "/home/toba/git/github/pslib/python/alp/veeam"
    destination_folder = "/home/toba/git/github/pslib/python/alp/s1"
    synchronize_folders(source_folder, destination_folder)
