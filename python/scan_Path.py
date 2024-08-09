import os
import platform
import time
import pandas as pd
import math
import sys

#------------------------------------------------------------#
# Add script to use 'install_modules' module
script_dir = 'e:\\Privat\\All Code\\Programs'
if script_dir not in sys.path:
    sys.path.append(script_dir)
    print(f"Added {script_dir} to path")
else:
    print(f"{script_dir} is already in path\n")
    print(sys.path)

import install_modules
install_modules.install_modules_of(os.path.abspath(__file__))
#------------------------------------------------------------#

start_time = time.time()

def system():
    print(platform.system(), end=" ")
    print(platform.release())
    print("Version:", platform.version())
    print(f"Processor: {platform.processor()}")
    print(f"Machine: {platform.machine()}")
    print(f"Python-Version: {platform.python_version()}")
    print("\n")

def convert_size(size_bytes):
    if size_bytes == 0:
        return "0B"
    size_name = ("B", "KB", "MB", "GB", "TB")
    i = int(math.floor(math.log(size_bytes, 1024)))
    p = math.pow(1024, i)
    s = round(size_bytes / p, 2)
    return f"{s} {size_name[i]}"

def save_to_file(file_format, summary_file_path, file_data):
    try:
        if file_format == "txt":
            with open(summary_file_path, "w") as summary_file:
                for file in file_data:
                    summary_file.write(f"{file['path']}\n")
        elif file_format == "csv":
            df = pd.DataFrame(file_data)
            df.to_csv(summary_file_path, index=False)
        elif file_format == "xlsx":
            df = pd.DataFrame(file_data)
            df.to_excel(summary_file_path, index=False)
        else:
            print("Unsupported file format")
    except Exception as e:
        print(f"Error saving file: {e}")

def main():
    # Define the default directory to scan
    default_dir = "E:\\Privat\\All Code\\"
    summary_dir = "E:\\Privat\\All Code\\Summary\\"

    # Blacklisted files and directories
    blacklisted = set(
        [
            "package.json",
            "config.json",
            "package-lock.json",
            "__pycache__",
            "node_modules",
            ".git",
            ".vscode",
            "venv",
            "LICENSE",
            "README.md",
            "README",
            ".gitignore",
            ".env",
            "Dell Vostro Mama",
        ]
    )

    # Get user input for the directory to scan
    inp = input(
        f'Enter the path of the folder you want to scan. If you don\'t type anything "{default_dir}" will be scanned: \n'
    )
    cwd = inp if inp else default_dir

    # Get user input for the file format to save
    file_format = (
        input("Enter the file format to save the summary (txt, csv, xlsx): ")
        .strip()
        .lower()
    )

    print(f'Scanning: "{cwd}"')

    # Ensure the summary directory exists
    os.makedirs(summary_dir, exist_ok=True)

    # Generate the summary file name
    scan_path_name = (cwd.strip(os.sep).split(os.sep)[-1]).replace(" ", "_")
    summary_file_name = f"summary__{scan_path_name}.{file_format}"
    summary_file_path = os.path.join(summary_dir, summary_file_name)

    file_data = []

    try:
        for root, dirs, file_names in os.walk(cwd):
            # Filter out blacklisted directories
            dirs[:] = [d for d in dirs if d not in blacklisted]

            for file_name in file_names:
                if file_name not in blacklisted:
                    # Construct the absolute file path
                    file_path = os.path.join(root, file_name)
                    file_size = os.path.getsize(file_path)
                    file_extension = os.path.splitext(file_name)[1]
                    directory_path = os.path.dirname(file_path)
                    file_title = os.path.splitext(file_name)[0]
                    file_data.append(
                        {
                            "path": file_path,
                            "directory": directory_path,
                            "name": file_name,
                            "title": file_title,
                            "type": file_extension,
                            "size": convert_size(file_size),
                        }
                    )
    except Exception as e:
        print(f"Error scanning directory: {e}")
        return

    # Save the data to the specified format
    save_to_file(file_format, summary_file_path, file_data)

    print(f"{len(file_data)} Files found.")
    print(f"Summary written to {summary_file_path}")

if __name__ == "__main__":
    system()
    main()
    time_elapsed = time.time() - start_time
    print(f"{time_elapsed:.3f} seconds")
