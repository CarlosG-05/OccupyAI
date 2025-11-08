from fastapi import FastAPI, Request
from fastapi.responses import JSONResponse
from supabase import create_client, Client
import os

app = FastAPI()

# Supabase credentials (set these as environment variables in Docker)
SUPABASE_URL = os.getenv("SUPABASE_URL")
SUPABASE_KEY = os.getenv("SUPABASE_KEY")
supabase: Client = create_client(SUPABASE_URL, SUPABASE_KEY)

@app.post("/data")
async def receive_data(request: Request):
    data = await request.json()
    print(f"Received data: {data}")
    # Insert data into Supabase (replace 'your_table' with your table name)
    try:
        response = supabase.table("study_rooms").insert(data).execute()
        return JSONResponse(content={"status": "success", "data": response.data})
    except Exception as e:
        return JSONResponse(content={"status": "error", "message": str(e)}, status_code=500)

@app.get("/")
def root():
    return {"message": "FastAPI server is running"}
    
if __name__ == "__main__":
    import uvicorn
    uvicorn.run("main:app", host="0.0.0.0", port=8000)
