import json
import os

# This code is for searching in all system directories and stored in the JSON file

def list_files(startpath):
    files_list = []
    for root, dirs, files in os.walk(startpath):
        for file in files:
            file_path = os.path.join(root, file)
            files_list.append(file_path)
    return files_list

def dir():
    startpath = "/"
    files_list = list_files(startpath)
    with open("files_list.json", "w", encoding='utf-8') as f:
        json.dump(files_list, f, ensure_ascii=False, indent=4)

dir()