import subprocess
import os
from dotenv import load_dotenv, find_dotenv

# Check for .env file
if not find_dotenv():
    print(".env file not found! Please create a .env file with PASSWORD_333, EDUROAM_USER, and EDUROAM_PASS.")
    exit(1)

load_dotenv()

SSID_333 = "333"
PASSWORD_333 = os.getenv("PASSWORD_333")
EDUROAM_SSID = "eduroam"
EDUROAM_USER = os.getenv("EDUROAM_USER")
EDUROAM_PASS = os.getenv("EDUROAM_PASS")

def scan_networks():
    result = subprocess.run(['nmcli', '-t', '-f', 'SSID', 'dev', 'wifi'], capture_output=True, text=True)
    ssids = [line.strip() for line in result.stdout.split('\n') if line.strip()]
    return ssids

def connect_ssid_333():
    print(f"Attempting to connect to {SSID_333}...")
    add_command = [
        "nmcli", "connection", "add", "type", "wifi", "con-name", SSID_333,
        "ifname", "wlan0", "ssid", SSID_333,
        "wifi-sec.key-mgmt", "wpa-psk", "wifi-sec.psk", PASSWORD_333
    ]
    activate_command = ["nmcli", "connection", "up", SSID_333]
    try:
        subprocess.run(add_command, check=True)
        subprocess.run(activate_command, check=True)
        print("Connection to 333 successful")
        return True
    except subprocess.CalledProcessError:
        print("Connection to 333 failed")
        return False
    except FileNotFoundError:
        print("Error: nmcli command not found")
        return False

def connect_eduroam():
    print(f"Attempting to connect to {EDUROAM_SSID} (eduroam enterprise)...")
    add_command = [
        "nmcli", "connection", "add", "type", "wifi", "con-name", EDUROAM_SSID,
        "ifname", "wlan0", "ssid", EDUROAM_SSID,
        "wifi-sec.key-mgmt", "wpa-eap",
        "802-1x.eap", "PEAP",
        "802-1x.phase2-auth", "MSCHAPV2",
        "802-1x.identity", EDUROAM_USER,
        "802-1x.password", EDUROAM_PASS
    ]
    activate_command = ["nmcli", "connection", "up", EDUROAM_SSID]
    try:
        subprocess.run(add_command, check=True)
        subprocess.run(activate_command, check=True)
        print("Connection to eduroam successful")
        return True
    except subprocess.CalledProcessError:
        print("Connection to eduroam failed")
        return False
    except FileNotFoundError:
        print("Error: nmcli command not found")
        return False

def main():
    ssids = scan_networks()
    if SSID_333 in ssids:
        if connect_ssid_333():
            return
    if EDUROAM_SSID in ssids:
        connect_eduroam()
    else:
        print("No target networks found.")

if __name__ == '__main__':
    main()
