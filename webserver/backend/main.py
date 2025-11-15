from fastapi import FastAPI, Request
from fastapi.staticfiles import StaticFiles
from fastapi.responses import JSONResponse
from supabase import create_client, Client
import uvicorn
import os
from datetime import datetime
from fastapi import BackgroundTasks

from contextlib import asynccontextmanager

@asynccontextmanager
async def lifespan(app):
    if os.getenv("RUN_SEED_ON_STARTUP") == "true":
        seed_if_empty()  # Runs at startup only in Docker
    yield

app = FastAPI(lifespan=lifespan)

app.mount("/main", StaticFiles(directory="./dist", html=True), name="static")

# Supabase credentials (set these as environment variables in Docker)
SUPABASE_URL = os.getenv("SUPABASE_URL")
SUPABASE_KEY = os.getenv("SUPABASE_KEY")
supabase: Client = create_client(SUPABASE_URL, SUPABASE_KEY)

def _make_room_payload(room_number: int, floor: int=1, building: str = "Love Library", capacity: int = 20, occupancy: int = 0):
    """Helper to create a study_rooms row payload."""
    return {
        "room_number": room_number,
        "floor": floor,
        "building": building,
        "capacity": capacity,
        "current_occupancy": occupancy
    }

def upload_dummy_data(count: int = 3):
    """Insert 10 hard-coded study room rows into Supabase `study_rooms` table for Love Library floor 1.

    Each room has capacity 4 and a random current occupancy (0-4).
    """
    payload = [
        # Floor 1 rooms
        {"room_number": 100, "floor": 1, "building": "Love Library", "capacity": 4, "current_occupancy": 0},
        {"room_number": 101, "floor": 1, "building": "Love Library", "capacity": 4, "current_occupancy": 1},
        {"room_number": 102, "floor": 1, "building": "Love Library", "capacity": 4, "current_occupancy": 2},
        {"room_number": 103, "floor": 1, "building": "Love Library", "capacity": 4, "current_occupancy": 3},
        {"room_number": 104, "floor": 1, "building": "Love Library", "capacity": 4, "current_occupancy": 4},
        {"room_number": 105, "floor": 1, "building": "Love Library", "capacity": 4, "current_occupancy": 2},
        {"room_number": 106, "floor": 1, "building": "Love Library", "capacity": 4, "current_occupancy": 1},
        {"room_number": 107, "floor": 1, "building": "Love Library", "capacity": 4, "current_occupancy": 0},
        {"room_number": 108, "floor": 1, "building": "Love Library", "capacity": 4, "current_occupancy": 3},
        {"room_number": 109, "floor": 1, "building": "Love Library", "capacity": 4, "current_occupancy": 4},
        # Floor 2 rooms
        {"room_number": 200, "floor": 2, "building": "Love Library", "capacity": 4, "current_occupancy": 1},
        {"room_number": 201, "floor": 2, "building": "Love Library", "capacity": 4, "current_occupancy": 2},
        {"room_number": 202, "floor": 2, "building": "Love Library", "capacity": 4, "current_occupancy": 3},
        {"room_number": 203, "floor": 2, "building": "Love Library", "capacity": 4, "current_occupancy": 4},
        {"room_number": 204, "floor": 2, "building": "Love Library", "capacity": 4, "current_occupancy": 0},
        {"room_number": 205, "floor": 2, "building": "Love Library", "capacity": 4, "current_occupancy": 2},
        {"room_number": 206, "floor": 2, "building": "Love Library", "capacity": 4, "current_occupancy": 1},
        {"room_number": 207, "floor": 2, "building": "Love Library", "capacity": 4, "current_occupancy": 0},
        {"room_number": 208, "floor": 2, "building": "Love Library", "capacity": 4, "current_occupancy": 3},
        {"room_number": 209, "floor": 2, "building": "Love Library", "capacity": 4, "current_occupancy": 4},
        # Floor 3 rooms (only first room uses 'LL-' prefix)
        {"room_number": "LL-312", "floor": 3, "building": "Love Library", "capacity": 4, "current_occupancy": 0},
        {"room_number": "314", "floor": 3, "building": "Love Library", "capacity": 4, "current_occupancy": 1},
        {"room_number": "321", "floor": 3, "building": "Love Library", "capacity": 4, "current_occupancy": 2},
        {"room_number": "323", "floor": 3, "building": "Love Library", "capacity": 4, "current_occupancy": 3},
        {"room_number": "331", "floor": 3, "building": "Love Library", "capacity": 4, "current_occupancy": 4},
        {"room_number": "333", "floor": 3, "building": "Love Library", "capacity": 4, "current_occupancy": 2},
        {"room_number": "334", "floor": 3, "building": "Love Library", "capacity": 4, "current_occupancy": 1},
        {"room_number": "336", "floor": 3, "building": "Love Library", "capacity": 4, "current_occupancy": 0},
        {"room_number": "366", "floor": 3, "building": "Love Library", "capacity": 4, "current_occupancy": 3},
        {"room_number": "369", "floor": 3, "building": "Love Library", "capacity": 4, "current_occupancy": 4},
        {"room_number": "370", "floor": 3, "building": "Love Library", "capacity": 4, "current_occupancy": 1},
        {"room_number": "372", "floor": 3, "building": "Love Library", "capacity": 4, "current_occupancy": 2},
        {"room_number": "376", "floor": 3, "building": "Love Library", "capacity": 4, "current_occupancy": 3},
        {"room_number": "378", "floor": 3, "building": "Love Library", "capacity": 4, "current_occupancy": 4},
        {"room_number": "381", "floor": 3, "building": "Love Library", "capacity": 4, "current_occupancy": 0},
        {"room_number": "383", "floor": 3, "building": "Love Library", "capacity": 4, "current_occupancy": 1},
        {"room_number": "385", "floor": 3, "building": "Love Library", "capacity": 4, "current_occupancy": 2},
        {"room_number": "387", "floor": 3, "building": "Love Library", "capacity": 4, "current_occupancy": 3},
        # Floor 4 rooms (only first room uses 'LL-' prefix)
        {"room_number": "LL-418", "floor": 4, "building": "Love Library", "capacity": 4, "current_occupancy": 4},
        {"room_number": "420", "floor": 4, "building": "Love Library", "capacity": 4, "current_occupancy": 2},
        {"room_number": "422", "floor": 4, "building": "Love Library", "capacity": 4, "current_occupancy": 1},
        {"room_number": "428B", "floor": 4, "building": "Love Library", "capacity": 4, "current_occupancy": 0},
        {"room_number": "428C", "floor": 4, "building": "Love Library", "capacity": 4, "current_occupancy": 3},
        {"room_number": "466", "floor": 4, "building": "Love Library", "capacity": 4, "current_occupancy": 4},
        {"room_number": "467", "floor": 4, "building": "Love Library", "capacity": 4, "current_occupancy": 2},
        {"room_number": "468", "floor": 4, "building": "Love Library", "capacity": 4, "current_occupancy": 1},
        {"room_number": "469", "floor": 4, "building": "Love Library", "capacity": 4, "current_occupancy": 0},
        {"room_number": "470", "floor": 4, "building": "Love Library", "capacity": 4, "current_occupancy": 3},
        {"room_number": "471", "floor": 4, "building": "Love Library", "capacity": 4, "current_occupancy": 4},
        # Floor 5 rooms (only first room uses 'LL-' prefix)
        {"room_number": "LL-517", "floor": 5, "building": "Love Library", "capacity": 4, "current_occupancy": 0},
        {"room_number": "530", "floor": 5, "building": "Love Library", "capacity": 4, "current_occupancy": 1},
        {"room_number": "530A", "floor": 5, "building": "Love Library", "capacity": 4, "current_occupancy": 2},
        {"room_number": "532", "floor": 5, "building": "Love Library", "capacity": 4, "current_occupancy": 3},
        {"room_number": "582", "floor": 5, "building": "Love Library", "capacity": 4, "current_occupancy": 4}
    ]

    # Insert into Supabase
    try:
        print("payload:", payload)
        resp = supabase.table("study_rooms").insert(payload).execute()
        return resp
    except Exception as e:
        # re-raise to let caller/endpoint handle the error
        raise

def seed_if_empty():
    print("Checking if study_rooms table needs seeding...")
    try:
        resp = supabase.table("study_rooms").select("id").limit(1).execute()
        if not resp.data:
            upload_dummy_data(count=3)
        else:
            print("study_rooms table already has data; skipping seed.")
    except Exception as e:
        print(f"[Startup seed] Error: {e}")

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

@app.get("/floor/{floor_number}")
def get_rooms_by_floor(floor_number: int):
    try:
        response = supabase.table("study_rooms").select("*").eq("floor", floor_number).execute()
        return JSONResponse(content={"status": "success", "data": response.data})
    except Exception as e:
        return JSONResponse(content={"status": "error", "message": str(e)}, status_code=500)
    
if __name__ == "__main__":
    uvicorn.run("main:app", host="0.0.0.0", port=8000)
