from fastapi import FastAPI
from fastapi.responses import StreamingResponse
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from api.chat import run_chat

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "https://clarissa-heinemann.de",
        "https://www.clarissa-heinemann.de",
        "http://localhost:8080"
    ],
    allow_methods=["POST"],
    allow_headers=["*"],
)

class ChatBody(BaseModel):
    messages: list[dict]

@app.post("/api/chat")
def chat(body: ChatBody):
    return StreamingResponse(run_chat(body.messages), media_type="text/plain")
