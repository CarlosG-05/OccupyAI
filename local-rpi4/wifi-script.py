import subprocess

#TODO: Move to .env
ssid = "SETUP-E811"
password = "block9357bucket"

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
    print("Connection added")

    print("Activating connection...")
    subprocess.run(activate_command, check=True)
    print("Successfully connected")
except subprocess.CalledProcessError:
    print("Connection failed")
except FileNotFoundError:
    print("nmcli command not found")
