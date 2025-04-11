import psutil
import hashlib
import os

CHUNK_SIZE = 65536

mount_points = []
files_of_dir = []


def hash_file(file):
    hasher = hashlib.sha256()
    with open(file, "rb") as f:
        content = f.read(CHUNK_SIZE)
        hasher.update(content)
    return hasher.hexdigest()


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

for root, dirs, files in os.walk(root_dir):
    if files:
        for i in files:
            file = os.path.join(root, i)
            if not os.path.islink(file):
                files_of_dir.append(file)
