from pathlib import Path
import shutil

base_dir = Path(__file__).parent
source_file = base_dir / "sample.txt"
backup_dir = base_dir / "backup"
backup_dir.mkdir(exist_ok=True)

copy_file = backup_dir / "sample_copy.txt"
backup_file = backup_dir / "sample_backup.txt"

if source_file.exists():
    shutil.copy(source_file, copy_file)
    print(f"Copied file to: {copy_file}")

    shutil.copy2(source_file, backup_file)
    print(f"Backup created at: {backup_file}")
else:
    print("Source file does not exist. Run write_files.py first.")

if copy_file.exists():
    copy_file.unlink()
    print(f"Deleted file: {copy_file}")
else:
    print("Copied file not found.")