import requests
from datetime import datetime

data = {
    "room_number": 101,
    "building": "Main Hall",
    "capacity": 20,
    "current_occupancy": 5,
    "last_updated": datetime.now().isoformat()
}

response = requests.post("http://localhost:8000/data", json=data)
print(response.json())