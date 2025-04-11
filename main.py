from os import dup
import drive_operations
import hashlib

CHUNK_SIZE = 65536  # Read files in 64kb chunks


def hash_file(filepath):
    """Calculates the SHA256 hash of a file."""
    hasher = hashlib.sha256()
    try:
        with open(filepath, "rb") as file:
            while True:
                chunk = file.read(CHUNK_SIZE)
                if not chunk:
                    break
                hasher.update(chunk)
        return hasher.hexdigest()
    except IOError as e:
        print(f"  Warning: Could not read file {filepath}: {e}")
        return None



def main():
    drives = drive_operations.get_names()
    selected_drive = drive_operations.get_selected(
        drives, "󰝤󰝤󰝤󰝤󰝤󰝤 Drives connected to the system 󰝤󰝤󰝤󰝤󰝤󰝤󰝤", "Select your drive: "
    )
    mount_point = drive_operations.get_mount_points(selected_drive)
    selected_mount_point = drive_operations.get_selected(
        mount_point,
        "󰝤󰝤󰝤󰝤󰝤󰝤 Mount points for your drive 󰝤󰝤󰝤󰝤󰝤󰝤󰝤",
        "Select a mountpoint: ",
    )
    every_damn_file = drive_operations.get_all_files(selected_mount_point)
    every_files_hash = []
    for file in every_damn_file:
        every_files_hash.append(hash_file(file))

    files_with_hash = {}
    for i in range(0, len(every_damn_file)):
        files_with_hash.update({every_files_hash[i]: every_damn_file[i]})


if __name__ == "__main__":
    main()
