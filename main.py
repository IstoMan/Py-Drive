import psutil
import hashlib
import os

CHUNK_SIZE = 65536


def hash_file(file):
    hasher = hashlib.sha256()
    with open(file, "rb") as f:
        content = f.read(CHUNK_SIZE)
        hasher.update(content)
    return hasher.hexdigest()


def create_hash_table(root_dir):
    hash_and_file = {}
    for root, dirs, files in os.walk(root_dir):
        if files:
            for i in files:
                file = os.path.join(root, i)
                if not os.path.islink(file):
                    hash = hash_file(file)
                    hash_and_file.update({file: hash})
    return hash_and_file


def main():
    mount_points = []
    print("Here are the connnect drives to your system: ")
    for disks in psutil.disk_partitions(all=False):
        mount_points.append(disks.mountpoint)

    for i, mount_point in enumerate(mount_points, start=1):
        print(f"{i}. {mount_point}")

    while True:
        try:
            selected_mountpoint = int(input("Enter your drive: ")) - 1
            break
        except ValueError:
            print("Invalid input, enter a number")

    root_dir = mount_points[selected_mountpoint]
    print(f"How have selected {root_dir}")

    hash_and_file = create_hash_table(root_dir)


if __name__ == "__main__":
    main()
