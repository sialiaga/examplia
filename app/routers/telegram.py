from typing import Literal
from fastapi import APIRouter, HTTPException, status
from pydantic import BaseModel
from ..service.websocket_manager import websocket_manager

telegram = APIRouter()

class authData(BaseModel):
    id: str

class InstructionMessage(BaseModel):
    id: str
    action: Literal["explain", "move"]
    desc: str


@telegram.post("/handshake/")
async def read_users(auth: authData):
    is_auth = await websocket_manager.is_connect(auth.id)
    if is_auth:
        return {"message": "User connected successfully"}
    else:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="User not connected or unauthorized"
        )
    
@telegram.post("/instruction/")
async def read_users(data: InstructionMessage):
    if not await websocket_manager.is_connect(data.id):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="User not connected or unauthorized."
        )

    response_payload = data.action + ":"

    # 2. Action Handling
    if data.action == "explain":
        try:
            # TODO: Implement actual GPT API call here
            # For now, using a placeholder.
            # gpt_response = await call_gpt_api(data.desc) 
            gpt_response = "This is a pending GPT explanation." 
            response_payload += gpt_response
        except Exception as e:
            # Log the error for debugging purposes
            print(f"Error calling GPT API: {e}") 
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail="Failed to get explanation from AI."
            )
    
    elif data.action == "move":
        if data.desc not in ["next", "prev"]:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Invalid 'move' operation. 'desc' must be 'next' or 'prev'."
            )
        response_payload += data.desc
    
    await websocket_manager.send_personal_message(response_payload, data.id)

    return {"message": "Operation successfully"}
