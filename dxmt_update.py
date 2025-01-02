# flake8: noqa
import os
import sys
import shutil
from pathlib import Path
from datetime import datetime
from typing import Iterable

def backup_and_overwrite(src_file, dest_file):
    backup_folder = os.path.join(os.path.dirname(dest_file), 'backup')
    if not os.path.exists(backup_folder):
        os.makedirs(backup_folder)

    backup_file = os.path.join(backup_folder, f"{os.path.basename(dest_file)}.{datetime.now().strftime('%Y%m%d%H%M%S')}")
    if os.path.exists(dest_file):
        shutil.move(dest_file, backup_file)
    shutil.copy2(src_file, dest_file)

def find_file_in_subfolders(src_folder, filename):
    for root, _, files in os.walk(src_folder):
        if filename in files:
            return os.path.join(root, filename)
    return None

def move_files(src_folder, wine_folder, wineprefix_folder):
    # as mentioned in https://github.com/3Shain/dxmt/wiki/DXMT-Installation-Guide-for-Geeks#movingreplacing-files
    files_to_move = {
        "winemetal.so": [os.path.join(wine_folder, "lib/wine/x86_64-unix/winemetal.so")],
        "winemetal.dll": [
            os.path.join(wine_folder, "lib/wine/x86_64-windows/winemetal.dll"),
            os.path.join(wineprefix_folder, "drive_c/windows/system32/winemetal.dll")
        ],
        "d3d11.dll": [os.path.join(wineprefix_folder, "drive_c/windows/system32/d3d11.dll")],
        "dxgi.dll": [os.path.join(wineprefix_folder, "drive_c/windows/system32/dxgi.dll")],
        "d3d10core.dll": [os.path.join(wineprefix_folder, "drive_c/windows/system32/d3d10core.dll")]
    }

    for filename, dest_files in files_to_move.items():
        src_file = find_file_in_subfolders(src_folder, filename)
        if src_file:
            for dest_file in dest_files:
                dest_dir = os.path.dirname(dest_file)
                if os.path.exists(dest_dir):
                    # compare the file hash, if different, backup and overwrite
                    if os.system(f"cmp -s {src_file} {dest_file}") == 0:
                            print(f"{src_file} and {dest_file} are the same, skip")
                            continue
                    backup_and_overwrite(src_file, dest_file)
                    print(f"{src_file} ==> {dest_file}")
                else:
                    print(f"Destination directory does not exist: {dest_dir}")
        else:
            print(f"Source file {filename} does not exist in {src_folder}")

def choose_items(item_list: Iterable[Path], item_name: str) -> Path:
    item_list = [i for i in item_list if not i.match(r'.*')]
    if len(item_list) == 0:
        raise ValueError(f"No {item_name} found")
    if len(item_list) == 1:
        return item_list[0]
    print(f"{item_name.capitalize()}s:")
    for i, item in enumerate(item_list):
        print(f"{i+1}. {item}")
    item_index = int(input(f"Enter the {item_name} index: "))
    return item_list[item_index-1]
    

if __name__ == "__main__":
    # search src_folder, src_folder should contains the dir: $(src_folder)/src/dxmt/
    if sys.argv[1:]:
        cur_folder = Path(sys.argv[1])
    else:
        cur_folder = Path()
    cur_folder = cur_folder.relative_to(".")
    src_folder = choose_items(Path.cwd().glob(f'{cur_folder}/**/src/dxmt/'), "dxmt folder").parent
    wine_folder = choose_items(Path("/Applications").glob('CrossOver*/Contents/SharedSupport/CrossOver/'), "wine folder")
    wineprefix_folder = choose_items(Path("/Users/qzhu/CXPBottles/").glob('*'), "bottle")
    
    move_files(src_folder, wine_folder, wineprefix_folder)