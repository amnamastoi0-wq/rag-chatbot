from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
import os
from dotenv import load_dotenv
from groq import Groq

load_dotenv()

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=False,
    allow_methods=["*"],
    allow_headers=["*"],
)

client = Groq(api_key=os.getenv("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"))

class Message(BaseModel):
    message: str
    session_id: str = None

@app.post("/chat")
async def chat(req: Message):
    try:
        response = client.chat.completions.create(
           model="llama-3.3-70b-versatile",
            messages=[
                {"role": "system", "content": "You are a helpful assistant that can answer anything."},
                {"role": "user", "content": req.message}
            ]
        )
        return {"reply": response.choices[0].message.content, "session_id": "default"}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))