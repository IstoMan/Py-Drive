import hashlib
from os import read
import drive_operations


def hash_gen_for_files(files: list) -> list:
    file_hash = []
    hash_md5 = hashlib.md5()
    for file in files:
        with open(file, "rb") as f:
            contents = f.read()
            hash_md5.update(contents)
            file_hash.append(hash_md5.hexdigest())
    return file_hash


def main():
    drives = drive_operations.get_names()
    selected_drive = drive_operations.get_selected(drives)
    mount_point = drive_operations.get_mount_points(selected_drive)
    selected_mount_point = drive_operations.get_selected(mount_point)
    every_damn_file = drive_operations.list_all_files(selected_mount_point)
    every_files_hash = hash_gen_for_files(every_damn_file)
    print(len(every_damn_file))
    print(len(every_files_hash))
    for i in range(0, len(every_damn_file)):
        file = every_damn_file[i]
        hash = every_files_hash[i]
        print(f"{file} (MD5) hash: {hash}")


if __name__ == "__main__":
    main()
