import xxhash
import drive_operations
import hashlib


def hash_gen_for_files(files: list) -> list:
    file_hash = []
    xx = xxhash.xxh64()
    for file in files:
        with open(file, "rb") as f:
            while chunk := f.read(8192):
                xx.update(chunk)
            file_hash.append(xx.hexdigest())
    return file_hash


def main():
    drives = drive_operations.get_names()
    selected_drive = drive_operations.get_selected(drives)
    mount_point = drive_operations.get_mount_points(selected_drive)
    selected_mount_point = drive_operations.get_selected(mount_point)
    every_damn_file = drive_operations.get_all_files(selected_mount_point)
    every_files_hash = hash_gen_for_files(every_damn_file)
    for i in range(0, len(every_damn_file)):
        file = every_damn_file[i]
        hash = every_files_hash[i]
        print(f"{file} (XXHASH) hash: {hash}")


if __name__ == "__main__":
    main()
