import subprocess
import os
from dotenv import load_dotenv

load_dotenv()

ssid = os.getenv("SSID")
password = os.getenv("PASSWORD")

add_command = ["nmcli",
               "connection",
               "add",
               "type",
               "wifi",
               "con-name",
               ssid,
               "ifname",
               "wlan0",
               "ssid",
               ssid,
               "wifi-sec.key-mgmt",
               "wpa-psk",
               "wifi-sec.psk",
               password
               ]

activate_command = ["nmcli",
                    "connection",
                    "up",
                    ssid
                    ]

try:
    print(f"Attempting to connect to {ssid}...")

    subprocess.run(add_command, check=True)
    subprocess.run(activate_command, check=True)

    print("Connection successful")
except subprocess.CalledProcessError:
    print("Connection failed")
except FileNotFoundError:
    print("Error: nmcli command not found")
