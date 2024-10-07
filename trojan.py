import subprocess
from scapy.all import ARP, Ether, srp
import socket
import pyautogui as pg
from time import sleep
from random import randint

# desired time for Delay
rand = randint(100,200)

def change_keyboard_language():
    pg.hotkey('alt', 'shift')
    sleep(10,30)
    pg.hotkey('alt', 'tab')
    
def change_ip_address(interface_name, new_ip, subnet_mask, gateway):
    try:
        subprocess.run(f'netsh interface ip set address "{interface_name}" static {new_ip} {subnet_mask} {gateway} 1', shell=True, check=True)
        
    except subprocess.CalledProcessError as e:
        pass
    
def toggle_internet():
    try:  
        subprocess.run('netsh interface set interface "Ethernet" admin=disable', shell=True, check=True)
        sleep(50)  
        subprocess.run('netsh interface ip set address name="Ethernet" static 192.168.80.200 255.255.255.0 192.168.80.1')
        subprocess.run('netsh interface set interface "Ethernet" admin=enable', shell=True, check=True)
    except subprocess.CalledProcessError as e:
        pass
    
def close_windows():
    pg.hotkey('alt', 'f4')
    pg.hotkey('Enter')
    
def scan_network(network_prefix, timeout=1, retries=3):
    # ساخت بسته ARP
    arp_request = ARP(pdst=f"{network_prefix}.1/24")
    ether = Ether(dst="ff:ff:ff:ff:ff:ff")
    packet = ether / arp_request
    devices = []
    for _ in range(retries):
        result = srp(packet, timeout=timeout, verbose=0)[0]
        for sent, received in result:
            device_info = {'ip': received.psrc, 'mac': received.hwsrc}
            try:
                hostname = socket.gethostbyaddr(received.psrc)[0]
                device_info['hostname'] = hostname
            except socket.herror:
                device_info['hostname'] = 'Unknown'
            if device_info not in devices:
                devices.append(device_info)
    return devices

def main():
    interface = "Ethernet"
    new_ip = "192.168.80.120"
    subnet_mask = "255.255.255.0"
    gateway = "192.168.80.1"
    while True:
        sleep(rand)
        toggle_internet()
        sleep(rand)
        change_ip_address(interface, new_ip, subnet_mask, gateway)
        sleep(rand)
        change_keyboard_language()
        sleep(rand)
        close_windows()
        sleep(rand)
        
        
sleep(600)

if __name__ == "__main__":
    main()
