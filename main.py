import psutil
import os

mount_points = []

print("Here are the connnect drives to your system: ")
for disks in psutil.disk_partitions(all=False):
    mount_points.append(disks.mountpoint)

for i in range(0, len(mount_points)):
    print(f"{i + 1}. {mount_points[i]}")

while True:
    try:
        selected_mountpoint = int(input("Enter your drive: ")) - 1
        break
    except ValueError:
        print("Invalid input, enter a number")

root_dir = mount_points[selected_mountpoint]
print(f"How have selected {root_dir}")

for root, dirs, files in os.walk(root_dir):
    print(files)
