import hashlib
import drive_operations


def main():
    drives = drive_operations.get_names()
    selected_drive = drive_operations.get_selected(drives)
    mount_point = drive_operations.get_mount_points(selected_drive)
    selected_mount_point = drive_operations.get_selected(mount_point)
    every_damn_file = drive_operations.list_all_files(selected_mount_point)


if __name__ == "__main__":
    main()
