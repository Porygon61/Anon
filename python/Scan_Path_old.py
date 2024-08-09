import sys
import os
import platform
import pywinctl as pwc
import pathlib as p
import time
import ipaddress as ip

start_time = time.time()

def system():
    print(platform.system(), end=' ')
    print(platform.release())
    print("Version:", platform.version())
    print(f'Processor: {platform.processor()}')
    print(f'Machine: {platform.machine()}')
    print(f'Python-Version: {platform.python_version()}')
    print('\n')

def main():
    
    file_location = os.path.abspath(__file__)
    blacklisted = ['summary.txt', 'package.json', 'package-lock.json', '__pycache__', 'node_modules', '.git', '.vscode', 'venv', 'LICENSE', 'README.md', 'README', '.gitignore', '.env']
    extensions = ['.txt', '.py', '.md', '', '.json', '.html', '.css', '.js', '.xml', '.exe', '' '.pdf', '.zip', '.png', '.jpg', '.gif', '.svg']
    inp = input('Enter the path of the folder you want to scan. If you dont type anything "E:\\Privat\\All Code\\" will be scanned: \n')
    if inp == '':
        cwd = 'E:\\Privat\\All Code\\'
    else:
        cwd = inp
    print(f'Scanning: "{cwd}"')
    
    objects = []
    os.chdir(cwd)
    objects = os.listdir(cwd)
    
    for object in objects:
        objects.remove(object)
        objects.insert(0, os.path.abspath(object))
        counter = len(objects) + 1
    while counter > len(objects):
        if counter - 1 == len(objects):
            counter -= 1
        for object in objects:
            file = os.path.basename(object).split('\\')[-1]
            if (os.path.isdir(object) and (file not in blacklisted)):
                objects.remove(object)
                counter -= 1
                os.chdir(object)
                new_objects = os.listdir(object)
                for new in new_objects:
                    objects.insert(0, os.path.abspath(new))
                    counter += 1
                new_objects.clear()
            elif os.path.isfile(object) and (object not in objects) and (file not in blacklisted):
                objects.append(object)
                counter += 1
                continue
            elif file in blacklisted:
                objects.remove(object)
                counter -= 1
                continue
            
    files = []
    files_count = 0
    if counter == len(objects):
        for object in objects:
            file = os.path.basename(object).split('\\')[-1]
            if os.path.isdir(object):
                objects.remove(object)
                counter -= 1
            else:
                if (os.path.isdir(file) == False) and file not in blacklisted:
                    files.append(object) #change object to file to only get names not paths
                    files_count += 1
        #files.sort(key=lambda x: os.path.splitext(x)[1]) #sort by file suffix 
        files.sort(key=lambda x: os.path.abspath(x)[0]) #sort by path
        
        summaryFile = open('E:\Privat\All Code\summary.txt', 'w')
        print(f'{"\n".join(files)}', file = summaryFile)
        summaryFile.close()
        print(f'{counter} Counts and {len(objects)} Objects')
        print(f'{len(files)} Files')
    
if __name__ == '__main__':
    system()
    main()
    time_elapsed = time.time() - start_time
    print(f'{time_elapsed:.3f} seconds')


