from fastapi import FastAPI, Request
import requests
import uuid

app = FastAPI()

@app.get('/messages')
def get_messages():
    return {"msg": "Not implemented yet."}