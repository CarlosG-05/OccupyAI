from fastapi import FastAPI, Request
from fastapi.staticfiles import StaticFiles
from fastapi.responses import JSONResponse
from supabase import create_client, Client
import uvicorn
import os
from datetime import datetime


from fastapi import BackgroundTasks
app = FastAPI()

app.mount("/main", StaticFiles(directory="./dist", html=True), name="static")

# Supabase credentials (set these as environment variables in Docker)
SUPABASE_URL = os.getenv("SUPABASE_URL")
SUPABASE_KEY = os.getenv("SUPABASE_KEY")
supabase: Client = create_client(SUPABASE_URL, SUPABASE_KEY)

def _make_room_payload(room_number: int, building: str = "Main Hall", capacity: int = 20, occupancy: int = 0):
    """Helper to create a study_rooms row payload."""
    return {
        "room_number": room_number,
        "building": building,
        "capacity": capacity,
        "current_occupancy": occupancy,
        "last_updated": datetime.now().isoformat() + 'Z'
    }

def upload_dummy_data(count: int = 3):
    """Insert `count` dummy study room rows into Supabase `study_rooms` table.

    Returns the Supabase response object.
    This function can be imported and called from tests or used by an endpoint.
    """
    payload = [
        _make_room_payload(room_number=100 + i, building=f"Building {i+1}", capacity=10 + i * 5, occupancy=(i % 4))
        for i in range(count)
    ]

    # Insert into Supabase
    try:
        resp = supabase.table("study_rooms").insert(payload).execute()
        return resp
    except Exception as e:
        # re-raise to let caller/endpoint handle the error
        raise

def seed_if_empty():
    try:
        resp = supabase.table("study_rooms").select("id").limit(1).execute()
        if not resp.data:
            upload_dummy_data(count=3)
            print("Seeded study_rooms with dummy data.")
        else:
            print("study_rooms table already has data; skipping seed.")
    except Exception as e:
        print(f"[Startup seed] Error: {e}")

seed_if_empty()

@app.post("/data")
async def receive_data(request: Request):
    data = await request.json()
    print(f"Received data: {data}")
    try:
        response = supabase.table("study_rooms").insert(data).execute()
        return JSONResponse(content={"status": "success", "data": response.data})
    except Exception as e:
        return JSONResponse(content={"status": "error", "message": str(e)}, status_code=500)
    
@app.get("/room/{room_id}")
def get_room(room_id: int):
    try:
        response = supabase.table("study_rooms").select("*").eq("room_number", room_id).execute()
        if response.data:
            return JSONResponse(content={"status": "success", "data": response.data[0]})
        else:
            print(f"Room with room_number {room_id} not found.")
            return JSONResponse(content={"status": "error", "message": "Room not found"}, status_code=404)
    except Exception as e:
        return JSONResponse(content={"status": "error", "message": str(e)}, status_code=500)

@app.get("/rooms")
def get_all_rooms():
    try:
        response = supabase.table("study_rooms").select("*").execute()
        return JSONResponse(content={"status": "success", "data": response.data})
    except Exception as e:
        return JSONResponse(content={"status": "error", "message": str(e)}, status_code=500)

if __name__ == "__main__":
    uvicorn.run("main:app", host="0.0.0.0", port=8000)
