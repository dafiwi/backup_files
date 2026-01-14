# Backup Files

This Python script creates backups of specified directories and files on an external data storage device (drive) like a USB stick or an external hard drive.
You can modify the directories and files in the script.
The script was tested successfully with Linux.

## ⚠️ Important Disclaimer

**USE AT YOUR OWN RISK!**

This Python script is provided "as is" without any warranties or guarantees.

- The author is **not responsible** for any data loss, file corruption, or other damages caused by using this script.
- **Always create a full backup** of your data before running the script.
- Test it on a copy of your files first.
- The script will not work as you wish if directory and file paths are not correct.

By using this script, you agree to assume all risks and indemnify the author from any claims.

## Notes

Use this script while only one external drive is connected to your system,
otherwise it will just use the first external drive it finds.

You will get an error if there are spaces in the external drive's name.

This script will not work if you try to backup your directories and files a second time on the same day and on the same external drive because it does not overwrite the backup directory.

Adjust directory and file paths in backup_files.py first before you execute the script (as described below) if you want to make changes (see comments).

## Tech Stack
- Python 3.10+
- Libraries: subprocess, os, shutil, pathlib, datetime, sys

## Installation
### Requirements
- Python 3.10 or higher.

git clone https://github.com/dafiwi/backup_files.git

cd path/to/script-directory

chmod +x backup_files.py
./backup_files.py

OR

python3 backup_files.py

OR

python backup_files.py

## License
This project is licensed under the MIT License. See [LICENSE](LICENSE). Copyright (c) dafiwi/2026 (https://github.com/dafiwi/backup_files).