import subprocess
import re
import json
import psutil

def get_wifi_profiles():
    profiles_data = subprocess.check_output('netsh wlan show profiles').decode('utf-8', errors="backslashreplace")
    profiles = re.findall("All User Profile     : (.*)\r", profiles_data)
    wifi_list = []
    for profile in profiles:
        profile_info = {}
        profile_info["Profile Name"] = profile

        try:
            profile_data = subprocess.check_output(f'netsh wlan show profile name="{profile}" key=clear').decode('utf-8', errors="backslashreplace")
            # Extracting relevant information
            ssid = re.search("SSID name              : (.*)\r", profile_data)
            key_content = re.search("Key Content            : (.*)\r", profile_data)
            authentication = re.search("Authentication         : (.*)\r", profile_data)
            cipher = re.search("Cipher                 : (.*)\r", profile_data)

            profile_info["SSID"] = ssid.group(1) if ssid else None
            profile_info["Password"] = key_content.group(1) if key_content else None
            profile_info["Authentication"] = authentication.group(1) if authentication else None
            profile_info["Cipher"] = cipher.group(1) if cipher else None

            wifi_list.append(profile_info)
        except subprocess.CalledProcessError:
            continue
    
    return wifi_list   

def wifi():
    wifi_profiles = get_wifi_profiles()
    
    with open("wifi_profiles.json", "w", encoding='utf-8') as f:
        json.dump(wifi_profiles, f, ensure_ascii=False, indent=4)     

def get_process_list():
    process_list = []
    for proc in psutil.process_iter(['pid', 'name', 'username', 'status']):
        try:
            process_info = proc.info
            process_list.append(process_info)
        except (psutil.NoSuchProcess, psutil.AccessDenied, psutil.ZombieProcess):
            continue
    return process_list

wifi()