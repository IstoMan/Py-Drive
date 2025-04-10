import subprocess
import json
import os
import sys
import hashlib

lsblk_output = subprocess.getoutput("lsblk -J")
block_devices_connected = json.loads(lsblk_output)

# TODO: Make this 2 functions into one and make make it recursive


def get_names() -> list:
    names_of_drives = []
    for drives in block_devices_connected.get("blockdevices", []):
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
    for devices in block_devices_connected.get("blockdevices", []):
        if devices["name"] == selected_drive:
            return devices["mountpoints"]
        else:
            if "children" in devices:
                for children in devices.get("children", []):
                    if children["name"] == selected_drive:
                        return children["mountpoints"]
                    else:
                        if "children" in children:
                            for child in children.get("children", []):
                                if child["name"] == selected_drive:
                                    return child["mountpoints"]


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


def list_all_files(drive_dir: str) -> list:
    raw_file_list = []
    nice_file_list = []
    for drive_dir, dirs, files in os.walk(drive_dir):
        # If is not a empty list then append it
        if files:
            raw_file_list.append(files)

    for i in raw_file_list:
        for j in i:
            nice_file_list.append(j)

    return nice_file_list


def main():
    drives = get_names()
    selected_drive = get_selected(drives)
    mount_point = get_mount_points(selected_drive)
    selected_mount_point = get_selected(mount_point)
    every_damn_file = list_all_files(selected_mount_point)


if __name__ == "__main__":
    main()
