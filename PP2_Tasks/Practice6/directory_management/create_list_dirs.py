from pathlib import Path
import os

base_dir = Path(__file__).parent
workspace = base_dir / "workspace"
nested_dir = workspace / "folder1" / "folder2" / "folder3"

# Create nested directories
nested_dir.mkdir(parents=True, exist_ok=True)
print(f"Created nested directories: {nested_dir}")

# Create sample files
file1 = workspace / "example1.txt"
file2 = workspace / "example2.py"
file3 = workspace / "example3.txt"

file1.write_text("This is a text file.", encoding="utf-8")
file2.write_text("print('Hello from Python')", encoding="utf-8")
file3.write_text("Another text file.", encoding="utf-8")

# Show current working directory
print("\nCurrent working directory:")
print(os.getcwd())

# List files and folders
print("\nFiles and folders in workspace:")
for item in os.listdir(workspace):
    print(item)

# Find files by extension
print("\nAll .txt files:")
for file in workspace.glob("*.txt"):
    print(file.name)