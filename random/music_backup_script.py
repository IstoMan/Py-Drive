import os
import shutil

home_directory = os.path.expanduser("~")
drive_dir = "/media/Suhas_s Backup/music/"
home_music_dir = f"{home_directory}/Music/"


def list_maker():
    drive = os.listdir(drive_dir)
    backup_dir = os.listdir(home_music_dir)
    unique_music = list(set(backup_dir) - set(drive))
    return unique_music


def main():
    music_not_saved = list_maker()
    if len(music_not_saved) != 0:
        try:
            for music in music_not_saved:
                destination_file = shutil.copy2(home_music_dir + music, drive_dir)
                print(f"File {music} has been copied to {destination_file}")
        except FileNotFoundError:
            print("File not Found")
        except Exception as e:
            print(f"An error occurred: {e}")
    else:
        print("The file have already been copied")


if __name__ == "__main__":
    main()
