import subprocess
import json
import sys
import os

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


def get_all_files(drive_dir: str) -> list:
    file_list = []
    for drive_dir, dirs, files in os.walk(drive_dir):
        if files:
            for i in files:
                full_path = os.path.join(drive_dir, i)
                file_list.append(full_path)

    return file_list
