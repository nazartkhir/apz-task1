from fastapi import FastAPI, Request
import requests
import uuid

app = FastAPI()

log_storage = {}

@app.post("/log")
async def log_message(request: Request):
    data = await request.json()
    msg_id = data.get('id')
    msg = data.get('msg')
    if not msg_id or not msg:
        return {"error": "Invalid data"}
    if msg_id in log_storage:
        print(f"Duplicate message detected: {msg_id}")
        return {"status": "duplicate"}
    log_storage[msg_id] = msg
    print(f"Logged: {msg_id} - {msg}")
    return {"status": "ok"}

@app.get("/logs")
def get_logs():
    logs_string = ', '.join([v for k, v in log_storage.items()])
    return {"msgs": logs_string}