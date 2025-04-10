import subprocess
import json
import os
import sys

lsblk_output = subprocess.getoutput("lsblk -J")
block_devices_connect = json.loads(lsblk_output)

# TODO: Make this 2 functions into one and make make it recursive


def get_names() -> list:
    names_of_drives = []
    for drives in block_devices_connect.get("blockdevices", []):
        if "name" in drives:
            names_of_drives.append((drives["name"]))
        if "children" in drives:
            for child in drives.get("children", []):
                if "name" in child:
                    names_of_drives.append((child["name"]))
                    if "children" in child:
                        for children in child.get("children", []):
                            names_of_drives.append((children["name"]))
    return names_of_drives


def get_mount_points(selected_drive):
    for drives in block_devices_connect.get("blockdevices", []):
        if drives["name"] == selected_drive:
            return drives["mountpoints"]
        if "children" in drives:
            for child in drives.get("children", []):
                if child["name"] == selected_drive:
                    return child["mountpoints"]
                if "children" in child:
                    for children in child.get("children", []):
                        return children["mountpoints"]


# TODO: Make it so that only mounted drives show up


def get_selected(selected_from):
    if len(selected_from) != 0:
        print("󰝤󰝤󰝤󰝤󰝤󰝤 Select one 󰝤󰝤󰝤󰝤󰝤󰝤󰝤")
        for i in range(0, len(selected_from)):
            print(f"{i + 1}. {selected_from[i]}")
        selected = int(input("Enter only one number: ")) - 1
        return selected_from[selected]
    else:
        sys.exit(1)


def list_files(drive_dir):
    raw_file_list = []
    nice_file_list = []
    index = 0
    for drive_dir, dirs, files in os.walk(drive_dir):
        if files:
            print(files)

    # # print(len(raw_file_list))
    # for i, j in raw_file_list:
    #     nice_file_list[index] = raw_file_list[i][j]
    #     index = index + 1

    # print(nice_file_list)
    # print(index)


def main():
    drives = get_names()
    selected_drive = get_selected(drives)
    mount_point = get_mount_points(selected_drive)
    selected_mount_point = get_selected(mount_point)
    list_files(selected_mount_point)


if __name__ == "__main__":
    main()
