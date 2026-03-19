from pathlib import Path

base_dir = Path(__file__).parent
file_path = base_dir / "sample.txt"

if file_path.exists():
    with open(file_path, "r", encoding="utf-8") as file:
        print("Using read():")
        print(file.read())

    with open(file_path, "r", encoding="utf-8") as file:
        print("\nUsing readline():")
        print(file.readline().strip())
        print(file.readline().strip())

    with open(file_path, "r", encoding="utf-8") as file:
        print("\nUsing readlines():")
        lines = file.readlines()
        for line in lines:
            print(line.strip())
else:
    print("File does not exist. Run write_files.py first.")