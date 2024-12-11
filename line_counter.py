from glob import glob

files = glob("*.py")
total_lines = 0
for file in files:
    if file != "line_counter.py":
        file_handle = open(file, "r")
        content = file_handle.readlines()
        content = [line for line in content if line != "\n"]
        file_handle.close()
        total_lines += len(content)

print(total_lines)
