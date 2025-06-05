# your_fastapi_project/api/websockets/router.py

import random 
import string
from fastapi import APIRouter, WebSocket, WebSocketDisconnect, HTTPException, status, Query
from ..service.websocket_manager import websocket_manager
from typing import Dict, Any, Optional
import json
import asyncio

websocket_router = APIRouter()


def generate_short_connection_id(length: int = 4) -> str:
    characters = string.ascii_uppercase + string.digits
    return ''.join(random.choice(characters) for i in range(length))

@websocket_router.websocket("/ws/{lesson_id}")
async def ws_connect(websocket: WebSocket, lesson_id: str):
    connection_id = generate_short_connection_id()
    print(f"Generando ID de conexión: {connection_id}") # Para depuración

    await websocket_manager.connect(websocket, lesson_id, connection_id)
    
    
    stop_event = asyncio.Event()

    try:
       await websocket.send_text(f"id:{connection_id}")
       await stop_event.wait() 

    except WebSocketDisconnect:

        print(f"Cliente {connection_id} (Lección: {lesson_id}) se desconectó.")
        await websocket_manager.disconnect(connection_id)
    
    except Exception as e:
        print(f"Error inesperado en WebSocket para {connection_id}: {e}")
        await websocket_manager.disconnect(connection_id)

@websocket_router.post("/test_action_ws/{connection_id}")
async def test_websocket_action(
    connection_id: str,
    action: str = Query(..., description="Action to perform (e.g., 'explain', 'move')"),
    desc: Optional[str] = Query(None, description="Description for the action (e.g., 'What is AI?', 'next', 'prev')")
):
    """
    Endpoint de prueba para enviar acciones directas a un cliente WebSocket.
    Se conecta a un cliente específico por connection_id y simula
    las acciones 'explain' o 'move'.
    """
    # 1. Connection Check
    if not await websocket_manager.is_connect(connection_id):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail=f"User with ID '{connection_id}' not connected."
        )

    response_payload = action + ":"

    # 2. Action Handling (Faked Logic)
    if action == "explain":
        try:
            # --- FAKED GPT API CALL ---
            if desc:
                gpt_response = f"This is a faked explanation for: '{desc}'. (AI Mock)"
            else:
                gpt_response = "This is a faked general explanation. (AI Mock)"
            response_payload += gpt_response
            # --- END FAKED GPT API CALL ---

        except Exception as e:
            print(f"Error calling GPT API (faked): {e}")
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail="Failed to get explanation from AI (faked error)."
            )

    elif action == "move":
        if desc not in ["next", "prev"]:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Invalid 'move' operation. 'desc' must be 'next' or 'prev'."
            )
        # --- FAKED MOVE LOGIC ---
        response_payload += desc
        # --- END FAKED MOVE LOGIC ---

    else:
        # Handle unsupported actions
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"Unsupported action: '{action}'. Allowed: 'explain', 'move'."
        )

    # 3. Send Response via WebSocket
    # Es crucial serializar el diccionario a una cadena JSON antes de enviarlo
    await websocket_manager.send_personal_message(json.dumps(response_payload), connection_id)

    return {"message": f"Action '{action}' for connection '{connection_id}' successfully executed and response sent via WebSocket."}