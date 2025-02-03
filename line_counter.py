import os


def count_lines_in_file(file_path):
    """
    Count the number of lines in a file.
    """
    try:
        with open(file_path, 'r', encoding='utf-8') as file:
            return sum(1 for line in file if line.strip())
    except Exception as e:
        print(f"Could not read file {file_path}: {e}")
        return 0


def scan_python_files(project_path, allowed_folders, excluded_folders):
    """
    Scan Python files in specific subfolders and count lines of code.
    """
    total_lines = 0
    file_line_counts = {}

    # Walk through the project path
    for dirpath, dirnames, filenames in os.walk(project_path):
        # Remove excluded folders from dirnames in-place to avoid descending into them
        dirnames[:] = [d for d in dirnames if d not in excluded_folders]

        # Check if the folder name is in the allowed list
        if any(allowed_folder in dirpath for allowed_folder in allowed_folders):
            for filename in filenames:
                if filename.endswith('.py'):  # Look for Python files
                    file_path = os.path.join(dirpath, filename)
                    line_count = count_lines_in_file(file_path)
                    total_lines += line_count
                    file_line_counts[file_path] = line_count

    return total_lines, file_line_counts

def main():
    # Input the project path
    project_path = os.path.abspath(os.path.dirname(__file__))

    if not os.path.exists(project_path):
        print("The provided path does not exist. Please try again.")
        return

    # Input the allowed subfolder names
    allowed_folders = ["assets", "config", "core", "database", "gui", "hardware", "utilities"]

    # Trim and clean folder names
    allowed_folders = [folder.strip() for folder in allowed_folders]
    excluded_folders = ["venv"]
    # Scan and count lines
    total_lines, file_line_counts = scan_python_files(project_path, allowed_folders, excluded_folders)

    # Output results
    print("\nLine Count per File:")
    for file_path, line_count in file_line_counts.items():
        print(f"{file_path}: {line_count} lines")

    print(f"\nTotal Lines of Code in Project: {total_lines} lines")

if __name__ == "__main__":
    main()
