from fastapi import FastAPI
from pydantic import BaseModel
import uvicorn

app = FastAPI()

class TranscriptionData(BaseModel):
    user_id: int
    text: str

@app.post("/transcription/")
async def receive_transcription(data: TranscriptionData):
    print(f"Recibí de usuario {data.user_id}: {data.text}")
    return {"status": "ok", "message": f"Transcripción recibida: {data.text}"}

if __name__ == "__main__":
    uvicorn.run("mock_api:app", host="127.0.0.1", port=8000, reload=True)
