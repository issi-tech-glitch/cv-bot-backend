from fastapi import FastAPI
from fastapi.responses import StreamingResponse
from pydantic import BaseModel
from api.chat import run_chat

app = FastAPI()

class ChatBody(BaseModel):
    messages: list[dict]

@app.post("/api/chat")
def chat(body: ChatBody):
    return StreamingResponse(run_chat(body.messages), media_type="text/plain")
