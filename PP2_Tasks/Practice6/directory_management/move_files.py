from pathlib import Path
import shutil

base_dir = Path(__file__).parent
source_dir = base_dir / "source"
destination_dir = base_dir / "destination"

source_dir.mkdir(exist_ok=True)
destination_dir.mkdir(exist_ok=True)

file1 = source_dir / "notes.txt"
file2 = source_dir / "report.txt"

file1.write_text("These are some notes.", encoding="utf-8")
file2.write_text("This is a report.", encoding="utf-8")

# Copy file
copied_path = destination_dir / file1.name
shutil.copy(file1, copied_path)
print(f"Copied {file1.name} to {copied_path}")

# Move file
moved_path = destination_dir / file2.name
shutil.move(str(file2), str(moved_path))
print(f"Moved {file2.name} to {moved_path}")

print("\nSource directory contents:")
for item in source_dir.iterdir():
    print(item.name)

print("\nDestination directory contents:")
for item in destination_dir.iterdir():
    print(item.name)