from pathlib import Path

# Папка, где лежит этот .py файл (file_handling)
base_dir = Path(__file__).parent

file_path = base_dir / "sample.txt"

# Write sample data
with open(file_path, "w", encoding="utf-8") as file:
    file.write("Alice, 85\n")
    file.write("Bob, 92\n")
    file.write("Charlie, 78\n")

print("Initial data written to file.")

# Append new lines
with open(file_path, "a", encoding="utf-8") as file:
    file.write("Diana, 88\n")
    file.write("Ethan, 95\n")

print("New lines appended.")

# Verify content
with open(file_path, "r", encoding="utf-8") as file:
    print("\nCurrent file content:")
    print(file.read())