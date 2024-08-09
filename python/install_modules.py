import sys
import os
import platform
import subprocess

#------------------------------------------------------------#
#---Script to use 'install_modules' module in another File---#
#------------------------------------------------------------#
#script_dir = 'e:\\Privat\\All Code\\Programs'
#if script_dir not in sys.path:
#    sys.path.append(script_dir)
#    print(f"Added {script_dir} to path")
#else:
#    print(f"{script_dir} is already in path\n")
#    print(sys.path)
#
#import install_modules
#install_modules.install_modules_of(os.path.abspath(__file__))
#------------------------------------------------------------#

def add_to_path():
    #script_dir = os.path.dirname(os.path.abspath(__file__))
    script_dir = 'g:\\Privat\\All Code\\Programs'       #CHANGE DRIVE BEFORE USE
    if script_dir not in sys.path:
        sys.path.append(script_dir)
        print(f"Added {script_dir} to path")
    else:
        print(f"{script_dir} is already in path\n")
        print(sys.path)

def check_py_version():
    python_version = platform.python_version().split(".")
    py_version = python_version[0] + python_version[1]
    if py_version == '':
        print("Please install Python from:\n\n(https://www.python.org/downloads/Windows).\nMAKE SURE TO ADD IT TO PATH !!!")
        sys.exit(1)
    return py_version

def install_modules_of(file_path): # check and install modules of the file given in file_path
    py_version = check_py_version()
    
    with open(file_path, "r") as file:
        lines = file.readlines()

    for line in lines:
        if line.startswith("import"):
            module = line.split()[1].strip()
            if module == 'install_modules':
                continue
            try:
                __import__(module)
            except ImportError:
                try:
                    subprocess.check_call([sys.executable, "-m", "pip", "install", module])
                except subprocess.CalledProcessError:
                    print(f"Error: Module {module} could not be installed.")
                    sys.exit(1)