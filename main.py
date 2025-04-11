import psutil
import sys
import os
import collections
import xxhash


CHUNK_SIZE = 65536


def get_mountpoins():
    mount_points = []
    print("Here are the connnect drives to your system: ")
    for disks in psutil.disk_partitions(all=False):
        mount_points.append(disks.mountpoint)

    for i, mount_point in enumerate(mount_points, start=1):
        print(f"{i}. {mount_point}")

    while True:
        try:
            selected_mountpoint: int = int(input("Enter your drive: ")) - 1
            if selected_mountpoint < 0 or selected_mountpoint > len(mount_points):
                print(f"Please enter a number between 1 and {len(mount_points)}")
            else:
                break
        except ValueError:
            print("Invalid input, enter a number")
        except KeyboardInterrupt:
            print("\nOperation cancelled by user.")
            sys.exit(0)

    root_dir = mount_points[selected_mountpoint]
    print(f"You have selected {root_dir}")
    return root_dir


def hash_file(file: str) -> str:
    hasher = xxhash.xxh64()
    with open(file, "rb") as f:
        content = f.read(CHUNK_SIZE)
        hasher.update(content)
    return hasher.hexdigest()


def create_hash_table(root_dir: str) -> dict:
    hash_and_file = collections.defaultdict(list)
    for root, dirs, files in os.walk(root_dir):
        if files:
            for i in files:
                file = os.path.join(root, i)
                if not os.path.islink(file):
                    hash = hash_file(file)
                    hash_and_file[hash].append(file)
    return hash_and_file


def get_duplicates(hashes_to_files: dict) -> dict:
    duplicated_dict = {}
    for file_hash, filenames in hashes_to_files.items():
        if len(filenames) > 1:
            duplicated_dict[file_hash] = filenames

    return duplicated_dict


def rename_or_delete(files: dict) -> None:
    options = ["d", "r", "s", "q"]
    while True:
        try:
            choice: str = input(
                "Enter d (Delete), r (Rename), s (Skip) or q (quit): "
            ).lower()
            if choice in options:
                break
            else:
                print("Enter valid input")
        except ValueError:
            print("Invalid input")
        except KeyboardInterrupt:
            print("\nOperation cancelled by user.")
            sys.exit(0)
    match choice:
        case "d":
            preserved_file = (
                int(
                    input(
                        "Enter the the file to be preserved, and rest will be deleted: "
                    )
                )
                - 1
            )
            for i in range(0, len(files)):
                if i == preserved_file:
                    pass
                else:
                    os.remove(files[i])
                    print("Deleted the files")
        case "r":
            preserved_file = (
                int(
                    input(
                        "Enter the the file to be preserved, and rest will be renamed: "
                    )
                )
                - 1
            )
            for i in range(0, len(files)):
                if i == preserved_file:
                    pass
                else:
                    os.rename(files[i], f"{files[i]}.bak")
                    print("Renamed the files")
        case "s":
            pass

        case "q":
            print("Exiting")
            sys.exit(1)


def main():
    # root_dir = get_mountpoins()
    root_dir = "/home/chad/testdir"
    hash_and_file = create_hash_table(root_dir)
    duplicates = get_duplicates(hash_and_file)
    for files in duplicates.values():
        for i, file in enumerate(files, 1):
            print(f"{i}. {file}")
        rename_or_delete(files)
        print("----------------")


if __name__ == "__main__":
    main()
