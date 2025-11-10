import requests
from datetime import datetime

data = {
    "room_number": 202,
    "building": "Main Hall",
    "capacity": 20,
    "current_occupancy": 5,
    "last_updated": datetime.now().isoformat()
}

#response = requests.post("http://localhost:8000/data", json=data)
#print(response.json())

#room_id = 6 # Change to the ID you want to fetch
url = f"http://localhost:8000/rooms"

response = requests.get(url)

try:
    response.raise_for_status()  # Raise an error for bad status codes
    print(response.json())
except requests.exceptions.HTTPError as e:
    print(f"Error: {e}")