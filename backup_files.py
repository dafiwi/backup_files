#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import subprocess
import os
import shutil
import pathlib
import datetime
import sys


# Adjust directories and files you want to backup here:
HOME_DIRECTORY = pathlib.Path.home()
SOURCES_DICTIONARY = {
    "SOURCE_DIRECTORY_1": HOME_DIRECTORY / "Documents" / "Work",
    "SOURCE_DIRECTORY_2": HOME_DIRECTORY / "Documents" / "other-stuff", 
    "SOURCE_FILE_1": HOME_DIRECTORY / "Documents" / "my-notes.txt",
    "SOURCE_FILE_2": HOME_DIRECTORY / "Documents" / "my-tables.xlsx"
}
BACKUP_DIRECTORY = f"files-backup-{datetime.date.today():%d-%m-%Y}"


def backup_files():

    print("\n************ BACKUP FILES ************\n")

    # Check all drives
    drives = subprocess.run(['lsblk', '-o', 'NAME,MOUNTPOINT,RM,TYPE,SIZE,FSTYPE'], 
                           capture_output=True, text=True)
    
    if drives.returncode != 0:
        print("\033[91mError while running lsblk\033[0m")
        return
    
    lines = drives.stdout.strip().split('\n')[1:]
    first_external_drive = None
    
    for line in lines:
        if not line.strip():
            continue
        parts = line.split()
        if len(parts) >= 3 and parts[2] == '1':
            drive_name = parts[0]
            mountpoint = parts[1] if len(parts) > 1 and parts[1] != '-' else None
            
            if first_external_drive is None:
                first_external_drive = {
                    'name': drive_name,
                    'mountpoint': mountpoint
                }
                break
    
    if not first_external_drive:
        print("\033[93mDid not find an external drive\033[0m")
        return
    
    print(f"External drive found: {first_external_drive['name']}")
    
    # Get mountpoint or find drive partition
    target_drive = None
    if (mountpoint := first_external_drive.get('mountpoint')) and mountpoint != '-':
        target_drive = mountpoint
    else:
        base_name = first_external_drive['name']
        for line in lines:
            if not line.strip():
                continue
            parts = line.split()
            if len(parts) >= 3 and parts[0].startswith(base_name) and len(parts) > 1 and parts[1] != '-':
                target_drive = parts[1]
                break
    
    if not target_drive:
        print("\033[93mNo drive mountpoint found\033[0m")
        return
    
    print(f"\033[92mUse mountpoint: {target_drive}\033[0m\n")
    
    targets = []

    # Check source directories and files
    sources_list = list(SOURCES_DICTIONARY.values())
    for item in sources_list:
        if not item.exists():
            print(f"{item}: Does not exist")
        elif item.is_dir():
            targets.append(item)
        elif item.is_file():
            targets.append(item)
        else:
            print(f"{item}: Is not a directory or a file")

    # Create target directory
    target_directory = pathlib.Path(target_drive) / BACKUP_DIRECTORY
    try:
        target_directory.mkdir(parents=True, exist_ok=False)
    except Exception as exception:
        print(f"\033[91mmkdir error: {exception}\033[0m")
        sys.exit(1)

    # Save directories and files on the external drive
    print("\nCopy directories and files ...\n")

    for item in targets:
        target_path = target_directory / item.name
        
        try:
            if item.is_dir():
                shutil.copytree(item, target_path, dirs_exist_ok=False)
                print(f"Copied directory: {item} to {target_path}")
            elif item.is_file():
                shutil.copy2(item, target_path)
                print(f"Copied file: {item} to {target_path}")
        except PermissionError:  
            print(f"\033[91m✗ {item.name}: PermissionError\033[0m")            
        except OSError as exception:
            print(f"\033[91m✗ {item.name}: OSError ({exception.errno})\033[0m")            
        except Exception as exception:
            print(f"\033[91m✗ {item.name}: {type(exception).__name__}: {exception}\033[0m")

    def has_backup_directory_any_content(target_directory):
        try:
            return any(os.scandir(target_directory))
        except (FileNotFoundError, NotADirectoryError):
            return False

    if has_backup_directory_any_content(target_directory):
        print("\n\033[92mAll listed directories and files were copied successfully.\033[0m")
        memory_size = (sum(os.path.getsize(file) for file in target_directory.rglob('*') if file.is_file())/1000/1000) + 0.1
        print(f"\033[96mThe backup directory has a memory size of {round(memory_size, 1)} MB.\033[0m\n")
    else:
        print("No directories or files were copied into the backup directory.\n")
    
if __name__ == "__main__":
    backup_files()