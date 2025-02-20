from fastapi import FastAPI, Request
import requests
import uuid
from tenacity import retry, stop_after_attempt, wait_fixed, before_log
import logging

app = FastAPI()

LOGGING_SERVICE_URL = 'http://127.0.0.1:5001/'
MESSAGE_SERVICE_URL = 'http://127.0.0.1:5002/'

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


@retry(stop=stop_after_attempt(3), wait=wait_fixed(2), before=lambda retry_state: logger.info("Sending message to logging service..."))
def send_with_retry(payload):
    response = requests.post(LOGGING_SERVICE_URL + 'log', json=payload)
    response.raise_for_status()
    return response.json()


@app.post("/send_message")
async def receive_message(request: Request):
    data = await request.json()
    msg = data.get('msg')
    if not msg:
        return {"error": "No message provided"}
    msg_id = str(uuid.uuid4())
    payload = {'id': msg_id, 'msg': msg}
    try:
        return send_with_retry(payload)
    except Exception as e:
        return {"error": "Failed to log message"} 

@app.get("/messages")
def get_messages():
    try:
        logging_response = requests.get(LOGGING_SERVICE_URL + 'logs')
        messages_response = requests.get(MESSAGE_SERVICE_URL + 'messages')
    except Exception as e:
        return {"error": "Failed to retrieve messages"}
    logging_msg = logging_response.json().get('msgs')
    messages = messages_response.json().get('msg')
    concat_msg = f"{logging_msg}, {messages}"
    return {"msgs": concat_msg}